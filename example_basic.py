import asyncio

from aidlab import AidlabManager, DataType, Device, DeviceDelegate, DisconnectReason


class MainManager(DeviceDelegate):
    async def run(self):
        devices = await AidlabManager().scan()
        if len(devices) > 0:
            print("Connecting to:", devices[0].address)
            await devices[0].connect(self)
            while True:
                await asyncio.sleep(1)

    def did_connect(self, device: Device):
        print("Connected to:", device.address)
        asyncio.create_task(device.collect([DataType.RESPIRATION], []))

    def did_disconnect(self, device: Device, reason: DisconnectReason):
        print("Disconnected from:", device.address, reason)

    def did_receive_respiration(self, device: Device, timestamp: int, value: float):
        print(value)

asyncio.run(MainManager().run())
