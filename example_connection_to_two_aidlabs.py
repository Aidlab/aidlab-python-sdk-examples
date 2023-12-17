import asyncio
from aidlab import AidlabManager, DataType, DeviceDelegate

FIRST_ADDRESS = "<YOUR FIRST DEVICE's ADDRESS>"
SECOND_ADDRESS = "<YOUR SECOND DEVICE's ADDRESS>"

class MainManager(DeviceDelegate):
    """Main class for managing devices."""

    async def run(self):
        devices = await AidlabManager().scan()
        if len(devices) > 0:
            first_device = next((device for device in devices if device.address == FIRST_ADDRESS), None)
            if first_device is not None:
                await devices[0].connect(self, [DataType.RESPIRATION])

            second_device = next((device for device in devices if device.address == SECOND_ADDRESS), None)
            if second_device is not None:
                await devices[1].connect(self, [DataType.RESPIRATION])

            while True:
                await asyncio.sleep(1)

    def did_connect(self, device):
        print("Connected to: ", device.address)

    def did_disconnect(self, device):
        print("Disconnected from: ", device.address)

    def did_receive_respiration(self, device, _, values):
        if device.address == FIRST_ADDRESS:
            print("Respiration: ", values, device.address)
        elif device.address == SECOND_ADDRESS:
            print("Respiration: ", values, device.address)

asyncio.run(MainManager().run())
