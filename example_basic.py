import Aidlab
from Aidlab.Signal import Signal

class MainManager(Aidlab.Aidlab):

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_respiration(self, aidlab, timestamp, values):
        print(values)


if __name__ == '__main__':
    signals = [Signal.respiration]

    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass
