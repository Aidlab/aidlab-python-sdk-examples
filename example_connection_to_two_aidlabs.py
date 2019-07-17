from Aidlab import AidlabBLECommunication as communication

first_address = "<YOUR FIRST AIDLAB's ADDRESS>"
second_address = "<YOUR SECOND AIDLAB's ADDRESS>"


class MainManager(communication.AidlabManager):

    def is_connected(self, address):
        print("Connected to: ", address)

    def is_disconnected(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def data_receiver(self, aidlab, characteristic_name, data):
        if aidlab.address == first_address:
            if characteristic_name == "battery":
                print("Battery: {}".format(data))
            elif characteristic_name == "respiration":
                print("Respiration: {}".format(data))
        elif aidlab.address == second_address:
            if characteristic_name == "battery":
                print("Battery: {}".format(data))
            elif characteristic_name == "respiration":
                print("Respiration: {}".format(data))


if __name__ == '__main__':

    characteristics = ["battery", "respiration"]

    main_manager = MainManager()
    main_manager.connect(characteristics)

    while True:
        pass
