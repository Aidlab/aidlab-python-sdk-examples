import asyncio
from typing import TypedDict

import pandas as pd

from aidlab import AidlabManager, DataType, Device, DeviceDelegate, DisconnectReason


class EcgSeries(TypedDict):
    timestamp: list[int]
    ecg: list[float]


class RespirationSeries(TypedDict):
    timestamp: list[int]
    respiration: list[float]

PATH = "./"
filename = "output.csv"

class MainManager(DeviceDelegate):

    def __init__(self):
        self.signals_data_ecg: EcgSeries = {"timestamp": [], "ecg": []}
        self.signals_data_respiration: RespirationSeries = {"timestamp": [], "respiration": []}

    async def run(self):
        devices = await AidlabManager().scan()
        if len(devices) > 0:
            print("Connecting to:", devices[0].address)
            await devices[0].connect(self)
            print("Going to save data to csv file after 10 seconds. Don't forget wear device.")
            await asyncio.sleep(10)
            self.save_to_csv()

    def did_connect(self, device: Device):
        print("Connected to:", device.address)
        asyncio.create_task(device.collect([DataType.ECG, DataType.RESPIRATION], []))

    def did_disconnect(self, device: Device, reason: DisconnectReason):
        print("Disconnected from:", device.address, reason)
        self.save_to_csv()

    def did_receive_ecg(self, _: Device, timestamp: int, value: float):
        self.signals_data_ecg["timestamp"].append(timestamp)
        self.signals_data_ecg["ecg"].append(value)

    def did_receive_respiration(self, _: Device, timestamp: int, value: float):
        self.signals_data_respiration["timestamp"].append(timestamp)
        self.signals_data_respiration["respiration"].append(value)

    def save_to_csv(self):
        df_ecg = pd.DataFrame(self.signals_data_ecg)
        df_respiration = pd.DataFrame(self.signals_data_respiration)
        df_combined = pd.merge_asof(df_ecg, df_respiration, on="timestamp")
        df_combined.to_csv(PATH + filename, mode="w", index=False, header=True)

asyncio.run(MainManager().run())
