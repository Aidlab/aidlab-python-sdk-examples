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
            second_device = next((device for device in devices if device.address == SECOND_ADDRESS), None)
            
            if first_device is not None:
                await first_device.connect(self)

            if second_device is not None:
                await second_device.connect(self)

            while True:
                await asyncio.sleep(1)

    async def did_connect(self, device):
        print("Connected to: ", device.address)
        if device.address == FIRST_ADDRESS:
            await device.collect([DataType.RESPIRATION], [])
        elif device.address == SECOND_ADDRESS:
            await device.collect([DataType.RESPIRATION], [])

    def did_disconnect(self, device):
        print("Disconnected from: ", device.address)

    def did_receive_respiration(self, device, _, value):
        if device.address == FIRST_ADDRESS:
            print("Respiration: ", value, device.address)
        elif device.address == SECOND_ADDRESS:
            print("Respiration: ", value, device.address)

asyncio.run(MainManager().run())
