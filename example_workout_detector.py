import Aidlab
from Aidlab.Signal import Signal

class WorkoutDetector(Aidlab.Aidlab):

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_detect_exercise(self, aidlab, exercise):
        print(exercise)
        
if __name__ == '__main__':
    signals = [Signal.motion, Signal.orientation]
    
    workout_detector = WorkoutDetector()
    workout_detector.connect(signals)