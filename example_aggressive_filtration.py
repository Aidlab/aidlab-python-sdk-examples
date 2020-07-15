from Aidlab.Aidlab import Aidlab


class MainManager(Aidlab):

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)
        aidlab.set_ecg_filtration_method("aggressive")

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_ecg(self, aidlab, timestamp, value):
        print(value)


if __name__ == '__main__':

    signals = ["ecg"]

    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass
