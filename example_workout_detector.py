from Aidlab import AidlabBLECommunication as communication
from ctypes import CFUNCTYPE

class WorkoutDetector(communication.AidlabManager):

    def is_connected(self, address):
        print("Connected to: ", address)

    @CFUNCTYPE(None)
    def pushup_callback():
        print("pushup")

    @CFUNCTYPE(None)
    def jump_callback():
        print("jump")

    @CFUNCTYPE(None)
    def situp_callback():
        print("situp")

    
if __name__ == '__main__':

    characteristics = ["motion"]
    workout_detector = WorkoutDetector()
    workout_detector.connect(characteristics)

    while True:
        pass