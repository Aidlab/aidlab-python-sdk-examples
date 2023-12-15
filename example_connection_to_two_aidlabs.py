from AidlabSDK import AidlabSDK
from AidlabSDK import Signal

first_address = "<YOUR FIRST AIDLAB's ADDRESS>"
second_address = "<YOUR SECOND AIDLAB's ADDRESS>"


class MainManager(AidlabSDK):

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_respiration(self, aidlab, timestamp, values):
        if aidlab.address == first_address:
            print("Respiration: ", values, aidlab.address)
        elif aidlab.address == second_address:
            print("Respiration: ", values, aidlab.address)

    def did_receive_battery_level(self, aidlab, state_of_charge):
        if aidlab.address == first_address:
            print("Battery: ", state_of_charge, aidlab.address)
        elif aidlab.address == second_address:
            print("Battery: ", state_of_charge, aidlab.address)

if __name__ == '__main__':
    signals = [Signal.battery, Signal.respiration]
    
    main_manager = MainManager()
    main_manager.connect(signals)