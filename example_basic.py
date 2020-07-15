from Aidlab.Aidlab import Aidlab


class MainManager(Aidlab):

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_respiration(self, aidlab, timestamp, value):
        print(value)


if __name__ == '__main__':

    signals = ["respiration"]

    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass
