import asyncio

from Plot import Plot

from aidlab import AidlabManager, DataType, Device, DeviceDelegate, DisconnectReason


class MainManager(DeviceDelegate):
    def __init__(self):
        self.plot = Plot()

    async def run(self):
        devices = await AidlabManager().scan()
        if len(devices) > 0:
            await devices[0].connect(self)
            while True:
                await asyncio.sleep(1)

    def did_connect(self, device: Device):
        print(f"Connected to: {device.address}. You need to wear device to see samples.")
        asyncio.create_task(device.collect([DataType.ECG], []))
        self.plot.add(0)

    def did_disconnect(self, device: Device, reason: DisconnectReason):
        print("Disconnected from: ", device.address, reason)

    def did_receive_ecg(self, device: Device, timestamp: int, value: float):
        self.plot.add(value)

asyncio.run(MainManager().run())
