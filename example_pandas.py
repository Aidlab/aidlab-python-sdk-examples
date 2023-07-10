import Aidlab
from Aidlab.Signal import Signal
import pandas as pd

PATH = "./"
filename = "output.csv"

class MainManager(Aidlab.Aidlab):

    def __init__(self):
        super().__init__()
        self.signals_data_ecg = {"timestamp": [], "ecg": []}
        self.signals_data_respiration = {"timestamp": [], "respiration": []}

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)
        self.save_to_csv()

    def save_to_csv(self):
        df_ecg = pd.DataFrame(self.signals_data_ecg)
        df_respiration = pd.DataFrame(self.signals_data_respiration)
        df_combined = pd.merge_asof(df_ecg, df_respiration, on='timestamp')
        df_combined.to_csv(PATH+filename, mode="w", index = False, header=True)
        
    def did_receive_ecg(self, aidlab, timestamp, values):
        self.signals_data_ecg["timestamp"].append(timestamp)
        self.signals_data_ecg["ecg"].append(values[0])

    def did_receive_respiration(self, aidlab, timestamp, values):
        self.signals_data_respiration["timestamp"].append(timestamp)
        self.signals_data_respiration["respiration"].append(values[0])


if __name__ == '__main__':

    try:
        signals = [Signal.ecg, Signal.respiration]
        main_manager = MainManager()
        main_manager.connect(signals)

    finally:
        main_manager.save_to_csv()
