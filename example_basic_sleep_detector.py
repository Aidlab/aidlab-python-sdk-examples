# Basic Sleep Detector utilizing Aidlab's motion sensor

import Aidlab
from time import sleep, time
from datetime import datetime

class MainManager(Aidlab.Aidlab):

    def __init__(self):
        super().__init__()
        self.startTimeOfSleepingPosition = 0
        self.isInSleepingPosition = False

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_quaternion(self, aidlab, timestamp, qw, qx, qy, qz):
        self.naiveSleepDetector([qw, qx, qy, qz])

    def naiveSleepDetector(self, value):

        quaternion = value[0:4]

        verticalOrientation = self.determineVerticalOrientation(
            quaternion[0], quaternion[1], quaternion[2], quaternion[3])

        # Sleep detection heuristic
        self.basicSleepDetector(verticalOrientation)

    def determineVerticalOrientation(self, qW, qX, qY, qZ):

        normalVec = self.normalVectorToUp(qW, qX, qY, qZ)

        if normalVec[2] >= 0.5:
            return "OrientationDown"
        elif normalVec[2] <= -0.5:
            return "OrientationUp"
        else:
            return "OrientationFront"

    def normalVectorToUp(self, qW, qX, qY, qZ):

        quat = self.multQuat(qW, qX, qY, qZ, 0, 0, 0, 1)
        quat = self.multQuat(quat[0], quat[1], quat[2], quat[3], qW, -qX, -qY, -qZ)

        return [quat[1], quat[2], quat[3]]

    def multQuat(self, w, x, y, z, qW, qX, qY, qZ):

        newW = w * qW - x * qX - y * qY - z * qZ
        newX = w * qX + x * qW + y * qZ - z * qY
        newY = w * qY + y * qW + z * qX - x * qZ
        newZ = w * qZ + z * qW + x * qY - y * qX

        return [newW, newX, newY, newZ]


    def basicSleepDetector(self, verticalOrientation):

        if (verticalOrientation == 'OrientationUp' or verticalOrientation == 'OrientationDown') and self.isInSleepingPosition == False:
            self.isInSleepingPosition = True
            self.startTimeOfSleepingPosition = time()

        elif verticalOrientation == 'OrientationFront' and self.isInSleepingPosition:
            self.startTimeOfSleepingPosition = 0
            self.isInSleepingPosition = False

        # Sleep detection heuristic:
        # We are sleeping if we are in sleeping position for longer than 10 minutes
        if self.isInSleepingPosition and (time() - self.startTimeOfSleepingPosition > 10 * 60):
            print("I am sleeping")


if __name__ == '__main__':

    signals = ["orientation"]

    main_manager = MainManager()
    main_manager.connect(signals)

    while True:
        pass



