import asyncio

from aidlab import AidlabManager, DataType, Device, DeviceDelegate, DeviceEvent, DisconnectReason, ExerciseEvent


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

    def did_receive_event(self, _: Device, event: DeviceEvent):
        # A plank is reported again when it ends; print it once.
        if isinstance(event, ExerciseEvent) and event.end_timestamp in (None, event.timestamp):
            print(event.exercise.name)

asyncio.run(MainManager().run())
