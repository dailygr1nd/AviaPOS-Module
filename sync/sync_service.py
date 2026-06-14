import requests


class SyncService:

    def __init__(

        self,

        endpoint: str

    ):

        self.endpoint = endpoint

    def sync_event(

        self,

        event

    ):

        payload = {

            "event_id":
                event.event_id,

            "event_type":
                event.event_type,

            "merchant_id":
                event.merchant_id,

            "timestamp":
                event.timestamp,

            "previous_hash":
                event.previous_hash,

            "payload_hash":
                event.payload_hash,

            "event_hash":
                event.event_hash,

            "payload":
                event.payload
        }

        response = requests.post(

            self.endpoint,

            json=payload,

            timeout=10

        )

        return response.status_code