import asyncio
from aidlab import AidlabManager, DataType, DeviceDelegate
from Plot import Plot

class MainManager(DeviceDelegate):
    def __init__(self):
        self.plot = Plot()

    async def run(self):
        devices = await AidlabManager().scan()
        if len(devices) > 0:
            await devices[0].connect(self, [DataType.ECG])
            while True:
                await asyncio.sleep(1)

    def did_connect(self, aidlab):
        print("Connected to: %s. You need to wear device to see samples.", aidlab.address)
        self.plot.add(0)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_ecg(self, aidlab, timestamp, values):
        self.plot.add(values[0])

asyncio.run(MainManager().run())
