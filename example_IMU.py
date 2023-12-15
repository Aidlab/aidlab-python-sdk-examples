from AidlabSDK import AidlabSDK
from AidlabSDK import Signal

class MotionDetector(AidlabSDK):

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_accelerometer(self, aidlab, timestamp, ax, ay, az):
        print("Accel: %.2f %.2f %.2f" % (ax, ay, az) )
    
    def did_receive_gyroscope(self, aidlab, timestamp, gx, gy, gz):
        print("Gyro: %.0f %.0f %.0f" % (gx, gy, gz) )

    def did_receive_magnetometer(self, aidlab, timestamp, mx, my, mz):
        print("Magn: %.0f %.0f %.0f" % (mx, my, mz) )
    
    def did_receive_orientation(self, aidlab, timestamp, roll, pitch, yaw):
        print("Orient", roll, pitch, yaw)

    def did_receive_quaternion(self, aidlab, timestamp, qw, qx, qy, qz):
        print("Quat:", qw, qx, qy, qz)
        
if __name__ == '__main__':
    signals = [Signal.motion, Signal.orientation]
    
    motion_detector = MotionDetector()
    motion_detector.connect(signals)
