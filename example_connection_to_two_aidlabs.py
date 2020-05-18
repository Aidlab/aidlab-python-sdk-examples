from Aidlab.Aidlab import Aidlab

first_address = "<YOUR FIRST AIDLAB's ADDRESS>"
second_address = "<YOUR SECOND AIDLAB's ADDRESS>"


class MainManager(Aidlab):

    def is_connected(self, aidlab_address):
        print("Connected to: ", aidlab_address)

    def is_disconnected(self, aidlab_address):
        print("Disconnected from: ", aidlab_address)

    def did_receive_respiration(self, value, timestamp, aidlab_address):
        if aidlab_address == first_address:
            print("Respiration: ", value, aidlab_address)
        elif aidlab_address == second_address:
            print("Respiration: ", value, aidlab_address)

    def did_receive_battery_level(self, stateOfCharge, aidlab_address):
        if aidlab_address == first_address:
            print("Battery: ", stateOfCharge, aidlab_address)
        elif aidlab_address == second_address:
            print("Battery: ", stateOfCharge, aidlab_address)

if __name__ == '__main__':

    characteristics = ["battery", "respiration"]

    main_manager = MainManager()
    main_manager.connect(characteristics)

    while True:
        pass