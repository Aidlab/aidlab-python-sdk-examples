import Aidlab
from Aidlab.Signal import Signal

class MainManager(Aidlab.Aidlab):

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)
        aidlab.start_synchronization()

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def sync_state_did_change(self, aidlab, sync_state):
        print(sync_state)

    def did_receive_unsynchronized_size(self, aidlab, unsynchronized_size):
        print(unsynchronized_size)

    def did_receive_past_ecg(self, aidlab, timestamp, values):
        pass

    def did_receive_past_skin_temperature(self, aidlab, timestamp, value):
        pass
        
if __name__ == '__main__':

    signals = []
    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass
