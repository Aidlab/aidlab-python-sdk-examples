from Aidlab.Aidlab import Aidlab
from Aidlab.Plot import Plot


class MainManager(Aidlab):

    def __init__(self):
        super().__init__()
        self.plot = Plot()

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_ecg(self, aidlab, timestamp, value):
        self.plot.add(value)


if __name__ == '__main__':

    signals = ["ecg"]

    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass
