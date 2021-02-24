import Aidlab
import pandas as pd

class MainManager(Aidlab.Aidlab):

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)
        self.signals_data = { "Ecg": [] }

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

        df = pd.DataFrame(self.signals_data, columns= ["Ecg"])
        df.to_csv ("YOUR PATH/filename.csv", index = False, header=True)
        
    def did_receive_ecg(self, aidlab, timestamp, values):
        for value in values:
            self.signals_data["Ecg"].append(value)
        
if __name__ == '__main__':

    signals = ["ecg"]
    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass
