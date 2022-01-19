import Aidlab
from Aidlab.Signal import Signal

class MainManager(Aidlab.Aidlab):

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)
        aidlab.set_ecg_filtration_method("aggressive")

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_ecg(self, aidlab, timestamp, values):
        print(values)


if __name__ == '__main__':

    signals = [Signal.ecg]

    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass
