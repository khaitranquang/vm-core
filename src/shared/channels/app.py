import time

from channels_redis.core import RedisChannelLayer


class AppRedisChannelLayer(RedisChannelLayer):
    """
    Custom RedisChannelLayer
    """

    async def group_presence(self, group):
        """
        Check a group exists or not
        :param group:
        :return:
        """
        # Check the input
        assert self.valid_group_name(group), "Group name not valid"
        # Get a connection to the right shard
        group_key = self._group_key(group)
        async with self.connection(self.consistent_hash(group)) as connection:
            is_presence = await connection.exists(group_key)
            return True if is_presence == 1 else False

    async def group_discard_all_channel(self, group):
        """
        Removes all channels from the named group
        :param group: (str) Group name
        :return:
        """
        assert self.valid_group_name(group), "Group name not valid"
        key = self._group_key(group)
        async with self.connection(self.consistent_hash(group)) as connection:
            await connection.zremrangebyscore(key, min=0, max=int(time.time()))

    async def group_discard_multiple_channels(self, group, channels):
        """
        Remove channels from the named group
        :param group: (str) Group name
        :param channels: (list) List channels
        :return:
        """
        print("Discard channels: ", channels)
        if not channels:
            return
        assert self.valid_group_name(group), "Group name not valid"
        for channel in channels:
            self.valid_channel_name(channel), "Channel name not valid"
        key = self._group_key(group)
        async with self.connection(self.consistent_hash(group)) as connection:
            first_channel = channels[0]
            other_channels = channels[1:]
            await connection.zrem(key, first_channel, *other_channels)

    async def group_add_multiple_channels(self, group, channels):
        """
        Add multiple channels to the group
        :param group: (str) Group name
        :param channels: (list) List channels
        :return:
        """
        # Check the inputs
        assert self.valid_group_name(group), "Group name not valid"
        for channel in channels:
            assert self.valid_channel_name(channel), "Channel name not valid"
        # Get a connection to the right shard
        group_key = self._group_key(group)
        async with self.connection(self.consistent_hash(group)) as connection:
            for channel in channels:
                # Add to group sorted set with creation time as timestamp
                await connection.zadd(group_key, time.time(), channel)
                # Set expiration to be group_expiry, since everything in
                # it at this point is guaranteed to expire before that
                await connection.expire(group_key, self.group_expiry)

    async def list_channels(self, group):
        """
        Get list channels of the group
        :param group: (str) Group name
        :return: list channels
        """
        assert self.valid_group_name(group), "Group name not valid"
        key = self._group_key(group)
        async with self.connection(self.consistent_hash(group)) as connection:
            channels = await connection.zrange(key, 0, -1)
            channels_str = []
            for c in channels:
                c_str = c.decode() if isinstance(c, bytes) else str(c)
                channels_str.append(c_str)
            return channels_str

    async def channel_cached_messages(self, channel):
        """
        Get all cached messages in the channel
        :param channel: (str) Channel name
        :return:
        """
        # Type check
        assert self.valid_channel_name(channel), "Channel name not valid"
        # If it's a process-local channel, strip off local part and stick full name in message
        channel_non_local_name = channel
        if "!" in channel:
            channel_non_local_name = self.non_local_name(channel)
        # Write out message into expiring key (avoids big items in list)
        channel_key = self.prefix + channel_non_local_name
        # Pick a connection to the right server - consistent for specific channels, random for general channels
        if "!" in channel:
            index = self.consistent_hash(channel)
        else:
            index = next(self._send_index_generator)
        async with self.connection(index) as connection:
            # Discard old messages based on expiry
            await connection.zremrangebyscore(
                channel_key, min=0, max=int(time.time()) - int(self.expiry)
            )
            # Get list messages from the channel
            messages = await connection.zrange(channel_key, 0, -1)
            deserializer_messages = [
                self.deserialize(message).get("data") for message in messages
            ]
            return deserializer_messages

    async def channel_remove_cached_messages(self, channel):
        """
        Remove cached messages  in the channel
        :param channel: (str) Channel name
        :return:
        """
        # Type check
        assert self.valid_channel_name(channel), "Channel name not valid"
        # If it's a process-local channel, strip off local part and stick full name in message
        channel_non_local_name = channel
        if "!" in channel:
            channel_non_local_name = self.non_local_name(channel)
        # Write out message into expiring key (avoids big items in list)
        channel_key = self.prefix + channel_non_local_name
        # Pick a connection to the right server - consistent for specific channels, random for general channels
        if "!" in channel:
            index = self.consistent_hash(channel)
        else:
            index = next(self._send_index_generator)
        async with self.connection(index) as connection:
            # Discard all messages
            await connection.zremrangebyscore(channel_key, min=0, max=int(time.time()))
