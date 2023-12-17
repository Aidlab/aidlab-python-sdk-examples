import asyncio

from aidlab import AidlabManager, DataType, DeviceDelegate

class MainManager(DeviceDelegate):
    async def run(self):
        devices = await AidlabManager().scan()
        if len(devices) > 0:
            print("Connecting to:", devices[0].address)
            await devices[0].connect(self, [DataType.RESPIRATION])
            while True:
                await asyncio.sleep(1)

    def did_connect(self, device):
        print("Connected to:", device.address)

    def did_disconnect(self, device):
        print("Disconnected from:", device.address)

    def did_receive_respiration(self, device, timestamp: int, values: list[float]):
        print(values)

asyncio.run(MainManager().run())
