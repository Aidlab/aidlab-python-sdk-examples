from Aidlab import AidlabBLECommunication as communication


class MainManager(communication.AidlabManager):

    def is_connected(self, address):
        print("Connected to: ", address)

    def is_disconnected(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def data_receiver(self, aidlab, characteristic_name, data):
        print(aidlab.address, characteristic_name, data)


if __name__ == '__main__':

    characteristics = ["respiration"]

    main_manager = MainManager()
    main_manager.connect(characteristics)

    while True:
        pass
