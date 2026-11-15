"""
Streams live Aidlab data to Lab Streaming Layer (LSL), one stream per signal and device.

Usage: python example_lsl.py [address ...]
Without addresses it streams from every Aidlab found.

Timestamps are the device's capture times moved to the LSL clock by one fixed offset, so they keep the device's even
spacing. Measured over an hour with Aidlab 2, they are late by a constant 0.1 s or more (the Bluetooth delay of the
first batch) and drift about 30 ms per hour against the computer's clock.
"""

import asyncio
import sys

from pylsl import IRREGULAR_RATE, StreamInfo, StreamOutlet, local_clock

from aidlab import AidlabManager, DataType, Device, DeviceDelegate, DisconnectReason

# LSL stream type: (channel labels, unit)
STREAMS = {
    "ECG": (["ECG"], "volts"),
    "Respiration": (["Respiration"], "ohms"),
    "HeartRate": (["HeartRate"], "bpm"),
    "RR": (["RR"], "milliseconds"),
    "Accelerometer": (["X", "Y", "Z"], "g"),
}


def create_outlets(device: Device) -> dict[str, StreamOutlet]:
    outlets = {}
    for stream_type, (labels, unit) in STREAMS.items():
        # Samples come in batches with their own timestamps, so the rate is left to the timestamps.
        info = StreamInfo(
            f"Aidlab {stream_type} {device.serial_number}",
            stream_type,
            len(labels),
            IRREGULAR_RATE,
            "float32",
            f"aidlab-{device.serial_number}-{stream_type}",
        )
        channels = info.desc().append_child("channels")
        for label in labels:
            channel = channels.append_child("channel")
            channel.append_child_value("label", label)
            channel.append_child_value("unit", unit)
        outlets[stream_type] = StreamOutlet(info)
    return outlets


class MainManager(DeviceDelegate):
    def __init__(self):
        self.outlets: dict[str, dict[str, StreamOutlet]] = {}
        # Seconds from each device's clock to the LSL clock.
        self.offsets: dict[str, float] = {}
        # Samples of the batch being received: (stream type, capture timestamp, sample).
        self.batches: dict[str, list[tuple[str, int, list[float]]]] = {}

    async def run(self, addresses: list[str]):
        devices = await AidlabManager().scan()
        if addresses:
            devices = [device for device in devices if device.address in addresses]
        if len(devices) == 0:
            print("No Aidlab found")
            return
        for device in devices:
            print("Connecting to:", device.address)
            await device.connect(self)
        while True:
            await asyncio.sleep(1)

    async def did_connect(self, device: Device):
        print("Connected to:", device.address)
        self.outlets[device.address] = create_outlets(device)
        self.batches[device.address] = []
        await device.collect(
            [DataType.ECG, DataType.RESPIRATION, DataType.HEART_RATE, DataType.RR, DataType.MOTION],
            [],
        )

    def did_disconnect(self, device: Device, reason: DisconnectReason):
        print("Disconnected from:", device.address, reason)

    def push(self, device: Device, stream_type: str, timestamp: int, sample: list[float]):
        batch = self.batches[device.address]
        if not batch:
            # The SDK delivers a batch in one go, so the whole batch is there when the loop runs this.
            asyncio.get_running_loop().call_soon(self.send_batch, device.address, local_clock())
        batch.append((stream_type, timestamp, sample))

    def send_batch(self, address: str, arrival: float):
        batch, self.batches[address] = self.batches[address], []
        if address not in self.offsets:
            # The device clock is set with one-second resolution, so its offset to the LSL clock comes from the
            # first batch, whose newest sample arrives right after its capture. It stays fixed: the timestamps
            # keep the device's even spacing and include the Bluetooth delay of that batch.
            newest = max(timestamp for _, timestamp, _ in batch)
            self.offsets[address] = arrival - newest / 1000
        for stream_type, timestamp, sample in batch:
            self.outlets[address][stream_type].push_sample(sample, timestamp / 1000 + self.offsets[address])

    def did_receive_ecg(self, device: Device, timestamp: int, value: float):
        self.push(device, "ECG", timestamp, [value])

    def did_receive_respiration(self, device: Device, timestamp: int, value: float):
        self.push(device, "Respiration", timestamp, [value])

    def did_receive_heart_rate(self, device: Device, timestamp: int, heart_rate: int):
        self.push(device, "HeartRate", timestamp, [heart_rate])

    def did_receive_rr(self, device: Device, timestamp: int, rr: int):
        self.push(device, "RR", timestamp, [rr])

    def did_receive_accelerometer(self, device: Device, timestamp: int, ax: float, ay: float, az: float):
        self.push(device, "Accelerometer", timestamp, [ax, ay, az])


asyncio.run(MainManager().run(sys.argv[1:]))
