import Aidlab

first_address = "<YOUR FIRST AIDLAB's ADDRESS>"
second_address = "<YOUR SECOND AIDLAB's ADDRESS>"


class MainManager(Aidlab.Aidlab):

    def is_connected(self, aidlab):
        print("Connected to: ", aidlab.address)

    def is_disconnected(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_respiration(self, aidlab, timestamp, values):
        if aidlab_address == first_address:
            print("Respiration: ", values, aidlab.address)
        elif aidlab_address == second_address:
            print("Respiration: ", values, aidlab.address)

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