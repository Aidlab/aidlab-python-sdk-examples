#
# Aidlab_SDK.py
# Aidlab-SDK
# Created by Szymon Gesicki on 09.05.2020.
#

from ctypes import *
import sys
import os


class AidlabSDK_ptr(Structure):
    pass


class AidlabSDK:

    sample_time_callback_type = CFUNCTYPE(None, c_void_p, c_float, c_uint64)
    respiration_rate_callback_type = CFUNCTYPE(None, c_void_p, c_uint32, c_uint64)
    motion_callback_type = CFUNCTYPE(None, c_void_p, c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_uint64)
    battery_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    steps_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint64)
    orientation_callback_type = CFUNCTYPE(None, c_void_p, c_float, c_float, c_float, c_uint64)
    wear_state_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    heart_rate_callback_type = CFUNCTYPE(None, c_void_p, POINTER(c_int), c_int, c_uint64)
    sound_volume_callback_type = CFUNCTYPE(None, c_void_p, c_uint16, c_uint64)
    workout_callback_type = CFUNCTYPE(None)

    activity_type = {
        1: "automotive",
        2: "walking",
        4: "running",
        8: "cycling",
        16: "still",
        32: "still"
    }

    wear_state_type = {
        0: "placed properly",
        1: "placed upside down"
    }

    def __init__(self, delegate, aidlab_address):
        self.delegate = delegate
        self.aidlab_address = aidlab_address

        # loading  python_sdk lib
        cwd = os.getcwd()
        if 'linux' in sys.platform:
            self.lib = cdll.LoadLibrary(cwd+"/Aidlab/python_sdk.so")
        elif 'win32' in sys.platform:
            self.lib = cdll.LoadLibrary(cwd+"/Aidlab/python_sdk.dll")
        elif 'darwin' in sys.platform:
            self.lib = cdll.LoadLibrary(cwd+"/Aidlab/python_sdk.dylib")
        else:
            raise RuntimeError(
                "Unsupported operating system: {}".format(sys.platform))

        self.lib.initial.restype = POINTER(AidlabSDK_ptr)

        self.aidlab_sdk_ptr = self.lib.initial()
        # setting up type of variables and return values
        self.setup_process_types()

    def calculate_temperature(self, data):
        self.lib.processTemperaturePackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_respiration(self, data):
        self.lib.processRespirationPackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_ecg(self, data):
        self.lib.processECGPackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_battery(self, data):
        self.lib.processBatteryPackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_motion(self, data):
        self.lib.processMotionPackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_activity(self, data):
        self.lib.processActivityPackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_orientation(self, data):
        self.lib.processOrientationPackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_steps(self, data):
        self.lib.processStepsPackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_heart_rate(self, data):
        self.lib.processHeartRatePackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_health_thermometer(self, data):
        self.lib.processHealthThermometerPackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def calculate_sound_volume(self, data):
        self.lib.processSoundVolumePackage(
            (c_uint8 * len(data))(*data), len(data), self.aidlab_sdk_ptr)

    def set_firmware_revision(self, firmware_revision):
        self.lib.setFirmwareRevision((c_uint8 * len(firmware_revision))(*firmware_revision.encode('utf-8')), len(firmware_revision), self.aidlab_sdk_ptr)

    def set_hardware_revision(self, hardware_revision):
        self.lib.setHardwareRevision((c_uint8 * len(hardware_revision))(*hardware_revision.encode('utf-8')), len(hardware_revision), self.aidlab_sdk_ptr)

    def set_ecg_filtration_method(self, aggressive_ecg_filtration):
        self.lib.setAggressiveECGFiltration(aggressive_ecg_filtration, self.aidlab_sdk_ptr)

    def destroy(self):
        self.lib.destroy(self.aidlab_sdk_ptr)

    def setup_user_callback(self):

        self.ecg_c_callback = self.sample_time_callback_type(self.ecg_callback)
        self.respiration_c_callback = self.sample_time_callback_type(self.respiration_callback)
        self.temperature_c_callback = self.sample_time_callback_type(self.temperature_callback)
        self.activity_c_callback = self.sample_time_callback_type(self.activity_callback)
        self.motion_c_callback = self.motion_callback_type(self.motion_callback)
        self.battery_c_callback = self.battery_callback_type(self.battery_callback)
        self.steps_c_callback = self.steps_callback_type(self.steps_callback)
        self.orientation_c_callback = self.orientation_callback_type(self.orientation_callback)
        self.respiration_rate_c_callback = self.respiration_rate_callback_type(self.respiration_rate_callback)
        self.lead_off_c_callback = self.wear_state_callback_type(self.wear_state_did_change)
        self.heart_rate_c_callback = self.heart_rate_callback_type(self.heart_rate_callback)
        self.sound_volume_c_callback = self.sound_volume_callback_type(self.sound_volume_callback)

        self.lib.initUserServiceCallback(self.ecg_c_callback, self.respiration_c_callback, self.temperature_c_callback,
                                         self.motion_c_callback, self.battery_c_callback, self.activity_c_callback,
                                         self.steps_c_callback, self.orientation_c_callback, self.respiration_rate_c_callback,
                                         self.lead_off_c_callback, self.heart_rate_c_callback, self.sound_volume_c_callback, self.aidlab_sdk_ptr)

    def setup_workout_callback(self):

        self.jump_c_callback = self.workout_callback_type(self.jump_callback)
        self.sit_up_c_callback = self.workout_callback_type(self.sit_up_callback)
        self.push_up_c_callback = self.workout_callback_type(self.push_up_callback)
        self.burpee_c_callback = self.workout_callback_type(self.burpee_callback)

        self.lib.initWorkoutCallback(self.jump_c_callback, self.push_up_c_callback,
                                     self.sit_up_c_callback, self.burpee_c_callback, self.aidlab_sdk_ptr)

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
                                                     self.motion_callback_type, self.battery_callback_type, self.sample_time_callback_type,
                                                     self.steps_callback_type, self.orientation_callback_type, self.respiration_rate_callback_type,
                                                     self.wear_state_callback_type, self.heart_rate_callback_type, c_void_p]
        self.lib.initUserServiceCallback.restype = None

        self.lib.initWorkoutCallback.argtypes = [self.workout_callback_type, self.workout_callback_type,
                                                 self.workout_callback_type, self.workout_callback_type, c_void_p]
        self.lib.initWorkoutCallback.restype = None

        self.lib.destroy.argtypes = [c_void_p]
        self.lib.destroy.restype = None

    def push_up_callback(self):
        self.delegate.did_detect_push_up(self.aidlab_address)

    def sit_up_callback(self):
        self.delegate.did_detect_sit_up(self.aidlab_address)

    def jump_callback(self):
        self.delegate.did_detect_jump(self.aidlab_address)

    def burpee_callback(self):
        self.delegate.did_detect_burpee(self.aidlab_address)

    def ecg_callback(self, context, value, timestamp):
        self.delegate.did_receive_ecg(value, timestamp, self.aidlab_address)

    def respiration_callback(self, context, value, timestamp):
        self.delegate.did_receive_respiration(value, timestamp, self.aidlab_address)

    def battery_callback(self, context, state_of_charge):
        self.delegate.did_receive_battery_level(state_of_charge, self.aidlab_address)

    def temperature_callback(self, context, skin_temperature, timestamp):
        self.delegate.did_receive_temperature(skin_temperature, timestamp, self.aidlab_address)

    def motion_callback(self, context, qw, qx, qy, qz, ax, ay, az, timestamp):
        self.delegate.did_receive_motion(qw, qx, qy, qz, ax, ay, az, timestamp, self.aidlab_address)

    def orientation_callback(self, context, roll, pitch, yaw, timestamp):
        self.delegate.did_receive_orientation(roll, pitch, yaw, timestamp, self.aidlab_address)

    def activity_callback(self, context, activity, timestamp):
        activity = self.activity_type.get(activity, "still")
        self.delegate.did_receive_activity(activity, timestamp, self.aidlab_address)

    def steps_callback(self, context, steps, timestamp):
        self.delegate.did_receive_steps(steps, timestamp, self.aidlab_address)

    def heart_rate_callback(self, context, hrv, heart_rate, timestamp):
        hrv = [hrv[i] for i in range(9)]
        self.delegate.did_receive_heart_rate(hrv, heart_rate, timestamp, self.aidlab_address)

    def respiration_rate_callback(self, context, value, timestamp):
        self.delegate.did_receive_respiration_rate(value, timestamp, self.aidlab_address)

    def wear_state_did_change(self, context, wear_state):
        wear_state = self.wear_state_type.get(wear_state, "detached")
        self.delegate.wear_state_did_change(wear_state, self.aidlab_address)

    def sound_volume_callback(self, context, sound_volume, timestamp):
        self.delegate.did_receive_sound_volume(sound_volume, timestamp, self.aidlab_address)
