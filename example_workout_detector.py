from Aidlab.Aidlab import Aidlab


class WorkoutDetector(Aidlab):

    def did_connect_aidlab(self, aidlab_address):
        print("Connected to: ", aidlab_address)

    def did_detect_push_up(self, aidlab_address):
        print("push-up", aidlab_address)

    def did_detect_jump(self, aidlab_address):
        print("jump ", aidlab_address)

    def did_detect_sit_up(self, aidlab_address):
        print("situp", aidlab_address)

    def did_detect_burpee(self, aidlab_address):
        print("burpee", aidlab_address)


if __name__ == '__main__':

    characteristics = ["motion"]
    workout_detector = WorkoutDetector()
    workout_detector.connect(characteristics)

    while True:
        pass
