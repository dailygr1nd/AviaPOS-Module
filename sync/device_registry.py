import uuid


class DeviceRegistry:

    def __init__(self):

        self.devices = {}

    def register(

        self,

        merchant_id: str,

        device_name: str

    ):

        device_id = str(
            uuid.uuid4()
        )

        self.devices[
            device_id
        ] = {

            "merchant_id":
                merchant_id,

            "device_name":
                device_name
        }

        return device_id

    def get_device(

        self,

        device_id: str

    ):

        return self.devices.get(
            device_id
        )