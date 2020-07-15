#
# Aidlab_SDK.py
# Aidlab-SDK
# Created by Szymon Gesicki on 09.05.2020.
#

from Aidlab.IAidlab import IAidlab
from ctypes import *
import sys
import os


class AidlabSDK_ptr(Structure):
    pass


class AidlabSDK:

    sample_time_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float)
    activity_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint8)
    respiration_rate_callback_type = CFUNCTYPE(None, c_void_p, c_uint32, c_uint64)
    accelerometer_callback_type = CFUNCTYPE(None, c_void_p, c_float, c_float, c_float, c_uint64)
    gyroscope_callback_type = CFUNCTYPE(None, c_void_p, c_float, c_float, c_float, c_uint64)
    magnetometer_callback_type = CFUNCTYPE(None, c_void_p, c_float, c_float, c_float, c_uint64)
    battery_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    steps_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint64)
    orientation_callback_type = CFUNCTYPE(None, c_void_p, c_float, c_float, c_float, c_uint64)
    quaternion_callback_type = CFUNCTYPE(None, c_void_p, c_float, c_float, c_float, c_float, c_uint64)
    wear_state_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    heart_rate_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, POINTER(c_int), c_int)
    sound_volume_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint16)
    exercise_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)

    Activity_type = {
        1: "automotive",
        2: "walking",
        4: "running",
        8: "cycling",
        16: "still",
        32: "still"
    }

    Wear_state_type = {
        0: "placed properly",
        1: "loose",
        2: "placed upside down",
        3: "detached"
    }

    Exercise = {
        0: "pushUp",
        1: "jump",
        2: "sitUp",
        3: "burpee"
    }

    ecgFiltrationMethod = {"normal": False, "aggressive": True}

    def __init__(self, delegate, aidlab_address):
        self.delegate = delegate

        self.aidlab = IAidlab(self)
        self.aidlab.address = aidlab_address

        # loading  python_sdk lib
        cwd = os.getcwd()
        if 'linux' in sys.platform:
            self.lib = cdll.LoadLibrary(cwd+"/Aidlab/python_sdk.so")
        elif 'win32' in sys.platform:
            self.lib = cdll.LoadLibrary(cwd+"/Aidlab/python_sdk.dll")
        elif 'darwin' in sys.platform:
            self.lib = cdll.LoadLibrary(cwd+"/Aidlab/python_sdk.dylib")
        else:
            raise RuntimeError("Unsupported operating system: {}".format(sys.platform))

        self.lib.initial.restype = POINTER(AidlabSDK_ptr)

        self.aidlab_sdk_ptr = self.lib.initial()
        # setting up type of variables and return values
        self.setup_process_types()

        

    def calculate_temperature(self, data):
        self.lib.processTemperaturePackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_respiration(self, data):
        self.lib.processRespirationPackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_ecg(self, data):
        self.lib.processECGPackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_battery(self, data):
        self.lib.processBatteryPackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_motion(self, data):
        self.lib.processMotionPackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_activity(self, data):
        self.lib.processActivityPackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_orientation(self, data):
        self.lib.processOrientationPackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_steps(self, data):
        self.lib.processStepsPackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_heart_rate(self, data):
        self.lib.processHeartRatePackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_health_thermometer(self, data):
        self.lib.processHealthThermometerPackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_sound_volume(self, data):
        self.lib.processSoundVolumePackage((c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def did_receive_firmware_revision(self, firmware_revision):
        self.lib.setFirmwareRevision((c_uint8 * len(firmware_revision))(*firmware_revision.encode('utf-8')), len(firmware_revision), self.aidlab_sdk_ptr)
        self.aidlab.firmware_revision = firmware_revision

    def did_receive_hardware_revision(self, hardware_revision):
        self.lib.setHardwareRevision((c_uint8 * len(hardware_revision))(*hardware_revision.encode('utf-8')), len(hardware_revision), self.aidlab_sdk_ptr)
        self.aidlab.hardware_revision = hardware_revision

    def did_receive_manufacture_name(self, manufacture_name):
        self.aidlab.manufacture_name = manufacture_name

    def did_receive_serial_number(self, serial_number):
        self.aidlab.serial_number = serial_number

    def set_ecg_filtration_method(self, method):
        self.lib.setAggressiveECGFiltration(self.ecgFiltrationMethod.get(method,False), self.aidlab_sdk_ptr)

    def destroy(self):
        self.lib.destroy(self.aidlab_sdk_ptr)

    def did_connect_aidlab(self):
        self.delegate.did_connect(self.aidlab)

    def did_disconnect_aidlab(self):
        self.delegate.did_disconnect(self.aidlab)

    def setup_user_callback(self):

        self.ecg_c_callback = self.sample_time_callback_type(self.ecg_callback)
        self.respiration_c_callback = self.sample_time_callback_type(self.respiration_callback)
        self.temperature_c_callback = self.sample_time_callback_type(self.temperature_callback)
        self.activity_c_callback = self.activity_callback_type(self.activity_callback)
        self.accelerometer_c_callback = self.accelerometer_callback_type(self.accelerometer_callback)
        self.gyroscope_c_callback = self.gyroscope_callback_type(self.gyroscope_callback)
        self.magnetometer_c_callback = self.magnetometer_callback_type(self.magnetometer_callback)
        self.battery_c_callback = self.battery_callback_type(self.battery_callback)
        self.steps_c_callback = self.steps_callback_type(self.steps_callback)
        self.orientation_c_callback = self.orientation_callback_type(self.orientation_callback)
        self.quaternion_c_callback = self.quaternion_callback_type(self.quaternion_callback)
        self.respiration_rate_c_callback = self.respiration_rate_callback_type(self.respiration_rate_callback)
        self.wear_state_c_callback = self.wear_state_callback_type(self.wear_state_did_change)
        self.heart_rate_c_callback = self.heart_rate_callback_type(self.heart_rate_callback)
        self.sound_volume_c_callback = self.sound_volume_callback_type(self.sound_volume_callback)
        self.exercise_c_callback = self.exercise_callback_type(self.exercise_callback)

        self.lib.initUserServiceCallback(self.ecg_c_callback, self.respiration_c_callback, self.temperature_c_callback,
                                         self.accelerometer_c_callback, self.gyroscope_c_callback, self.magnetometer_c_callback,
                                         self.battery_c_callback, self.activity_c_callback, self.steps_c_callback, 
                                         self.orientation_c_callback, self.quaternion_c_callback, self.respiration_rate_c_callback,
                                         self.wear_state_c_callback, self.heart_rate_c_callback, self.sound_volume_c_callback,
                                         self.exercise_c_callback, self.aidlab_sdk_ptr)

    def setup_process_types(self):

        self.lib.processECGPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processECGPackage.restype = None

        self.lib.processTemperaturePackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processTemperaturePackage.restype = None

        self.lib.processMotionPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processMotionPackage.restype = None

        self.lib.processRespirationPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processRespirationPackage.restype = None

        self.lib.processBatteryPackage.argtypes = [ POINTER(c_uint8), c_int, c_void_p]
        self.lib.processBatteryPackage.restype = None

        self.lib.processActivityPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processActivityPackage.restype = None

        self.lib.processStepsPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processStepsPackage.restype = None

        self.lib.processOrientationPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processOrientationPackage.restype = None

        self.lib.processHeartRatePackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processHeartRatePackage.restype = None

        self.lib.setHardwareRevision.argtypes = [POINTER(c_uint8), c_void_p]
        self.lib.setHardwareRevision.restype = None

        self.lib.setFirmwareRevision.argtypes = [POINTER(c_uint8), c_void_p]
        self.lib.setFirmwareRevision.restype = None

        self.lib.setAggressiveECGFiltration.argtypes = [c_bool, c_void_p]
        self.lib.setAggressiveECGFiltration.restype = None

        self.lib.initUserServiceCallback.argtypes = [self.sample_time_callback_type, self.sample_time_callback_type, self.sample_time_callback_type,
                                                     self.accelerometer_callback_type, self.gyroscope_callback_type, self.magnetometer_callback_type,
                                                     self.battery_callback_type, self.activity_callback_type, self.steps_callback_type,
                                                     self.orientation_callback_type, self.quaternion_callback_type, self.respiration_rate_callback_type,
                                                     self.wear_state_callback_type, self.heart_rate_callback_type, self.sound_volume_callback_type,
                                                     self.exercise_callback_type, c_void_p]
        self.lib.initUserServiceCallback.restype = None

        self.lib.destroy.argtypes = [c_void_p]
        self.lib.destroy.restype = None

    def exercise_callback(self, context, exercise):
        exercise = self.Exercise.get(exercise, "None")
        self.delegate.did_detect_exercise(self.aidlab, exercise)
        
    def ecg_callback(self, context, timestamp, value):
        self.delegate.did_receive_ecg(self.aidlab, timestamp, value)

    def respiration_callback(self, context, timestamp, value):
        self.delegate.did_receive_respiration(self.aidlab, timestamp, value)

    def battery_callback(self, context, state_of_charge):
        self.delegate.did_receive_battery_level(self.aidlab, state_of_charge)

    def temperature_callback(self, context, timestamp, value):
        self.delegate.did_receive_skin_temperature(self.aidlab, timestamp, value)

    def accelerometer_callback(self, context, ax, ay, az, timestamp):
        self.delegate.did_receive_accelerometer(self.aidlab, timestamp, ax, ay, az)

    def gyroscope_callback(self, context, gx, gy, gz, timestamp):
        self.delegate.did_receive_gyroscope(self.aidlab, timestamp, gx, gy, gz)

    def magnetometer_callback(self, context, mx, my, mz, timestamp):
        self.delegate.did_receive_magnetometer(self.aidlab, timestamp, mx, my, mz)

    def orientation_callback(self, context, roll, pitch, yaw, timestamp):
        self.delegate.did_receive_orientation(self.aidlab, timestamp, roll, pitch, yaw)

    def quaternion_callback(self, context, qw, qx, qy, qz, timestamp):
        self.delegate.did_receive_quaternion(self.aidlab, timestamp, qw, qx, qy, qz)

    def activity_callback(self, context, timestamp, activity):
        activity = self.Activity_type.get(activity, "still")
        self.delegate.did_receive_activity(self.aidlab, timestamp, activity)

    def steps_callback(self, context, timestamp, value):
        self.delegate.did_receive_steps(self.aidlab, timestamp, value)

    def heart_rate_callback(self, context, timestamp, hrv, heart_rate):
        hrv = [hrv[i] for i in range(9)]
        self.delegate.did_receive_heart_rate(self.aidlab, timestamp, hrv, heart_rate)

    def respiration_rate_callback(self, context, timestamp, value):
        self.delegate.did_receive_respiration_rate(self.aidlab, timestamp, value)

    def wear_state_did_change(self, context, wear_state):
        wear_state = self.Wear_state_type.get(wear_state, "detached")
        self.delegate.wear_state_did_change(self.aidlab, wear_state)

    def sound_volume_callback(self, context, timestamp, sound_volume):
        self.delegate.did_receive_sound_volume(self.aidlab, timestamp, sound_volume)
