from Aidlab.Aidlab import Aidlab


class MainManager(Aidlab):

    def did_connect_aidlab(self, aidlab_address):
        print("Connected to: ", aidlab_address)

    def did_disconnect_aidlab(self, aidlab_address):
        print("Disconnected from: ", aidlab_address)

    def did_receive_ecg(self, value, timestamp, aidlab_address):
        print(value)


if __name__ == '__main__':

    characteristics = ["ecg"]

    main_manager = MainManager()
    main_manager.set_ecg_filtration_method("aggressive")
    main_manager.connect(characteristics)

    while True:
        pass
