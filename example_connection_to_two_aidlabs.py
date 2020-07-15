from Aidlab.Aidlab import Aidlab

first_address = "<YOUR FIRST AIDLAB's ADDRESS>"
second_address = "<YOUR SECOND AIDLAB's ADDRESS>"


class MainManager(Aidlab):

    def is_connected(self, aidlab):
        print("Connected to: ", aidlab.address)

    def is_disconnected(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_respiration(self, aidlab, timestamp, value):
        if aidlab_address == first_address:
            print("Respiration: ", value, aidlab.address)
        elif aidlab_address == second_address:
            print("Respiration: ", value, aidlab.address)

    def did_receive_battery_level(self, aidlab, stateOfCharge):
        if aidlab_address == first_address:
            print("Battery: ", stateOfCharge, aidlab.address)
        elif aidlab_address == second_address:
            print("Battery: ", stateOfCharge, aidlab.address)

if __name__ == '__main__':

    signals = ["battery", "respiration"]

    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass