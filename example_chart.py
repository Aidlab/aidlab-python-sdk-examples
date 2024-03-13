import asyncio
from aidlab import AidlabManager, DataType, DeviceDelegate
from Plot import Plot

class MainManager(DeviceDelegate):
    def __init__(self):
        self.plot = Plot()

    async def run(self):
        devices = await AidlabManager().scan()
        if len(devices) > 0:
            await devices[0].connect(self)
            while True:
                await asyncio.sleep(1)

    async def did_connect(self, device):
        print("Connected to: %s. You need to wear device to see samples.", device.address)
        await device.collect([DataType.ECG], [])
        self.plot.add(0)

    def did_disconnect(self, device):
        print("Disconnected from: ", device.address)

    def did_receive_ecg(self, device, timestamp, values):
        self.plot.add(values[0])

asyncio.run(MainManager().run())
