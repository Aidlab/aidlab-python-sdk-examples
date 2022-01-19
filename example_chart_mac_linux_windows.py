import Aidlab
from Aidlab.Signal import Signal
from Plot import Plot

class MainManager(Aidlab.Aidlab):

    def __init__(self):
        super().__init__()
        self.plot = Plot()

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_ecg(self, aidlab, timestamp, values):
        self.plot.add(values[0])


if __name__ == '__main__':

    signals = [Signal.ecg]

    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass
