"""
Basic Sleep Detector utilizing Aidlab's motion sensor
"""
import asyncio
from time import time

from aidlab import AidlabManager, DeviceDelegate, DataType

class MainManager(DeviceDelegate):

    def __init__(self):
        self.start_time_of_sleeping_position = 0
        self.is_in_sleeping_position = False

    async def run(self):
        devices = await AidlabManager().scan()
        if len(devices) > 0:
            print("Connecting to: ", devices[0].address)
            await devices[0].connect(self, [DataType.ORIENTATION])
            while True:
                await asyncio.sleep(1)

    def did_connect(self, device):
        print("Connected to: ", device.address)

    def did_disconnect(self, device):
        print("Disconnected from: ", device.address)

    def did_receive_quaternion(self, _, __, q_w, q_x, q_y, q_z):
        self.naive_sleep_detector([q_w, q_x, q_y, q_z])

    def naive_sleep_detector(self, value):

        quaternion = value[0:4]

        vertical_orientation = self.determine_vertical_orientation(
            quaternion[0], quaternion[1], quaternion[2], quaternion[3])

        # Sleep detection heuristic
        self.basic_sleep_detector(vertical_orientation)

    def determine_vertical_orientation(self, q_w, q_x, q_y, q_z):

        normal_vec = self.normal_vector_to_up(q_w, q_x, q_y, q_z)

        if normal_vec[2] >= 0.5:
            return "OrientationDown"
        if normal_vec[2] <= -0.5:
            return "OrientationUp"

        return "OrientationFront"

    def normal_vector_to_up(self, q_w, q_x, q_y, q_z):

        quat = self.mult_quat(q_w, q_x, q_y, q_z, 0, 0, 0, 1)
        quat = self.mult_quat(quat[0], quat[1], quat[2], quat[3], q_w, -q_x, -q_y, -q_z)

        return [quat[1], quat[2], quat[3]]

    def mult_quat(self, w, x, y, z, q_w, q_x, q_y, q_z):

        new_w = w * q_w - x * q_x - y * q_y - z * q_z
        new_x = w * q_x + x * q_w + y * q_z - z * q_y
        new_y = w * q_y + y * q_w + z * q_x - x * q_z
        new_z = w * q_z + z * q_w + x * q_y - y * q_x

        return [new_w, new_x, new_y, new_z]

    def basic_sleep_detector(self, vertical_orientation):

        if (vertical_orientation == 'OrientationUp' or vertical_orientation == 'OrientationDown') and self.is_in_sleeping_position == False:
            self.is_in_sleeping_position = True
            self.start_time_of_sleeping_position = time()

        elif vertical_orientation == 'OrientationFront' and self.is_in_sleeping_position:
            self.start_time_of_sleeping_position = 0
            self.is_in_sleeping_position = False

        # Sleep detection heuristic:
        # We are sleeping if we are in sleeping position for longer than 10 minutes
        if self.is_in_sleeping_position and (time() - self.start_time_of_sleeping_position > 10 * 60):
            print("I am sleeping")

asyncio.run(MainManager().run())
