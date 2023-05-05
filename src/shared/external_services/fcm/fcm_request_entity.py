from typing import List


class FCMRequestEntity:
    def __init__(self, collapse_key: str = None, time_to_live: bool = None, delay_while_idle: bool = False,
                 registration_ids: List[str] = None, data=None, priority: str = None):
        self._collapse_key = collapse_key
        self._time_to_live = time_to_live
        self._delay_while_idle = delay_while_idle
        self._registration_ids = registration_ids if registration_ids else []
        self._data = data
        self._priority = priority

    @property
    def collapse_key(self):
        return self._collapse_key

    @property
    def time_to_live(self):
        return self._time_to_live

    @property
    def delay_while_idle(self):
        return self._delay_while_idle

    @property
    def registration_ids(self):
        return self._registration_ids

    @registration_ids.setter
    def registration_ids(self, registration_ids_value: List[str]):
        self._registration_ids = registration_ids_value

    @property
    def data(self):
        return self._data

    @property
    def priority(self):
        return self._priority

    def to_json(self):
        return {
            "collapse_key": self.collapse_key,
            "time_to_live": self.time_to_live,
            "delay_while_idle": self.delay_while_idle,
            "registration_ids": self.registration_ids,
            "data": self.data,
            "priority": self.priority
        }

    def to_json_value_str(self):
        return {
            "collapse_key": str(self.collapse_key),
            "time_to_live": str(self.time_to_live),
            "delay_while_idle": str(self.delay_while_idle),
            "registration_ids": str(self.registration_ids),
            "data": str(self.data),
            "priority": str(self.priority)
        }

    def add_registration_id(self, registration_id):
        self._registration_ids.append(registration_id)

    def remove_registration_id(self, registration_id):
        self._registration_ids.remove(registration_id)

    def clear_registration_ids(self):
        self._registration_ids = []

    def data_part(self, key, value):
        self._data.update({key: value})
