import asyncio
from aidlab import AidlabManager, DataType, DeviceDelegate
import pandas as pd

PATH = "./"
filename = "output.csv"

class MainManager(DeviceDelegate):

    def __init__(self):
        self.signals_data_ecg = {"timestamp": [], "ecg": []}
        self.signals_data_respiration = {"timestamp": [], "respiration": []}

    async def run(self):
        devices = await AidlabManager().scan()
        if len(devices) > 0:
            print("Connecting to:", devices[0].address)
            await devices[0].connect(self, [DataType.ECG, DataType.RESPIRATION])
            print("Going to save data to csv file after 10 seconds. Don't forget wear device.")
            await asyncio.sleep(10)
            self.save_to_csv()

    def did_connect(self, device):
        print("Connected to:", device.address)

    def did_disconnect(self, device):
        print("Disconnected from:", device.address)
        self.save_to_csv()
        
    def did_receive_ecg(self, _, timestamp, values):
        self.signals_data_ecg["timestamp"].append(timestamp)
        self.signals_data_ecg["ecg"].append(values[0])

    def did_receive_respiration(self, _, timestamp, values):
        self.signals_data_respiration["timestamp"].append(timestamp)
        self.signals_data_respiration["respiration"].append(values[0])

    def save_to_csv(self):
        df_ecg = pd.DataFrame(self.signals_data_ecg)
        df_respiration = pd.DataFrame(self.signals_data_respiration)
        df_combined = pd.merge_asof(df_ecg, df_respiration, on='timestamp')
        df_combined.to_csv(PATH+filename, mode="w", index = False, header=True)

asyncio.run(MainManager().run())
