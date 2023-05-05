import json
import traceback
from firebase_admin import messaging

from shared.external_services.fcm.fcm_request_entity import FCMRequestEntity
from shared.log.cylog import CyLog
from shared.background.i_background import BackgroundThread


class FCMSenderService:
    def __init__(self, is_background=True):
        self.is_background = is_background

    @staticmethod
    def log_error(func_name: str = "", meta="", tb=None):
        if not tb:
            tb = traceback.format_exc()
        CyLog.error(**{"message": "[BACKGROUND] Function {} {} error: {}".format(func_name, meta, tb)})

    def run(self, func_name: str, **kwargs):
        # Get self-function by function name
        func = getattr(self, func_name)
        if not func:
            raise Exception("Func name {} does not exist in this background".format(func_name))
        if not callable(func):
            raise Exception("Func name {} is not callable".format(func_name))

        # Run background or not this function
        if self.is_background:
            BackgroundThread(task=func, **kwargs)
        else:
            func(**kwargs)

    def send_message(self, fcm_message) -> tuple:
        """
        Sending notification to multiple devices
        :param fcm_message:
        :return: (tuple) success_registration_id, failed_registration_id
        """
        if isinstance(fcm_message, FCMRequestEntity):
            fcm_message = fcm_message.to_json()
        registration_ids = list(set(fcm_message.get("registration_ids", [])))
        if not registration_ids:
            return [], []

        fcm_message_data = fcm_message.get("data")
        if "data" in fcm_message_data:
            fcm_message_data["data"] = json.dumps(fcm_message_data["data"])

        failed_registration_ids = []
        success_registration_ids = registration_ids.copy()

        batch_size = 450
        for i in range(0, len(registration_ids), batch_size):
            batch_registration_ids = registration_ids[i:i+batch_size]
            message = messaging.MulticastMessage(
                data=fcm_message_data,
                tokens=batch_registration_ids,
                android=messaging.AndroidConfig(
                    priority=fcm_message.get("priority") or "high"
                ),
                apns=messaging.APNSConfig(
                    headers={
                        'apns-push-type': 'background',
                        'apns-priority': '5',
                        'apns-topic': 'io.cystack.ready'
                    },
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(content_available=True)
                    )
                )
            )
            response = messaging.send_multicast(message)
            if response.failure_count > 0:
                responses = response.responses
                for idx, resp in enumerate(responses):
                    if not resp.success:
                        failed_registration_ids.append(batch_registration_ids[idx])
                        success_registration_ids.remove(batch_registration_ids[idx])

        print("success; ", success_registration_ids, failed_registration_ids)
        return success_registration_ids, failed_registration_ids

    def send_message_topic(self, topic: str, fcm_message):
        """
        Sending notification to multiple devices
        :param topic: (str) Topic name
        :param fcm_message:
        :return: (tuple) success_registration_id, failed_registration_id
        """
        if isinstance(fcm_message, FCMRequestEntity):
            fcm_message = fcm_message.to_json()

        fcm_message_data = fcm_message.get("data")
        if "data" in fcm_message_data:
            fcm_message_data["data"] = json.dumps(fcm_message_data["data"])

        message = messaging.Message(
            data=fcm_message_data,
            topic=topic,
            android=messaging.AndroidConfig(
                priority=fcm_message.get("priority") or "high"
            ),
            apns=messaging.APNSConfig(
                headers={
                    'apns-push-type': 'background',
                    'apns-priority': '5',
                    'apns-topic': 'io.cystack.ready'
                },
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(content_available=True)
                )
            )
        )
        response = messaging.send(message)
        print("Successfully sent message to topic: ", topic, response)

    def send_batch_messages(self, fcm_messages) -> tuple:
        """
        Sending notification to multiple devices
        :param fcm_messages: List FCMRequest Entity
        :return: (tuple) success_registration_id, failed_registration_id
        """
        messages = []
        failed_registration_ids = []
        success_registration_ids = []

        for fcm_message in fcm_messages:
            if isinstance(fcm_message, FCMRequestEntity):
                fcm_message = fcm_message.to_json()
            registration_ids = list(set(fcm_message.get("registration_ids", [])))
            if not registration_ids:
                continue

            success_registration_ids += registration_ids
            # Convert data to string
            fcm_message_data = fcm_message.get("data")
            if "data" in fcm_message_data:
                fcm_message_data["data"] = json.dumps(fcm_message_data["data"])

            message = messaging.Message(
                data=fcm_message_data,
                token=registration_ids[0],
                android=messaging.AndroidConfig(
                    priority=fcm_message.get("priority") or "high"
                ),
                apns=messaging.APNSConfig(
                    headers={
                        'apns-push-type': 'background',
                        'apns-priority': '5',
                        'apns-topic': 'io.cystack.ready'
                    },
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(content_available=True)
                    )
                )
            )
            messages.append(message)

        batch_size = 450
        for i in range(0, len(messages), batch_size):
            batch_messages = messages[i:i+batch_size]
            response = messaging.send_all(batch_messages)
            if response.failure_count > 0:
                responses = response.responses
                for idx, resp in enumerate(responses):
                    if not resp.success:
                        failed_registration_ids.append(batch_messages[idx].token)
                        success_registration_ids.remove(batch_messages[idx].token)

        print("success; ", success_registration_ids, failed_registration_ids)
        return success_registration_ids, failed_registration_ids
