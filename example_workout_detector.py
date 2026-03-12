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
        asyncio.create_task(device.collect([DataType.MOTION, DataType.ORIENTATION], []))

    def did_disconnect(self, device: Device, reason: DisconnectReason):
        print("Disconnected from:", device.address, reason)

    def did_detect_exercise(self, _: Device, exercise):
        print(exercise)

asyncio.run(MainManager().run())
