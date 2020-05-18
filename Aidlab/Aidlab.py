#
# Aidlab.py
# Aidlab-SDK
# Created by Szymon Gesicki on 09.05.2020.
#

from Aidlab.AidlabSDK import AidlabSDK
from Aidlab.AidlabPeripheral import AidlabPeripheral

class Aidlab:

    device_information = {}
    ecgFiltrationMethod = {"normal": False, "aggressive": True}

    def __init__(self):
        # Container for AidlabSDK libs
        self.aidlab_sdk = {}

        # default filtration method
        self.filtrationMethod = self.ecgFiltrationMethod.get("normal",False)

        self.aidlab_peripheral = AidlabPeripheral(self)

    def create_aidlabSDK(self, aidlab_address):

        self.aidlab_sdk[aidlab_address] = AidlabSDK(self, aidlab_address)

        self.aidlab_sdk[aidlab_address].set_ecg_filtration_method(self.filtrationMethod)
        self.aidlab_sdk[aidlab_address].setup_workout_callback()
        self.aidlab_sdk[aidlab_address].setup_user_callback()

    def destroy(self, aidlab_address):
        self.aidlab_sdk[aidlab_address].destroy()

    def connect(self, characteristics, aidlabsMAC=None):
        self.aidlab_peripheral.run(characteristics, aidlabsMAC)

    def set_ecg_filtration_method(self, ecg_filtration_method):
        self.filtrationMethod = self.ecgFiltrationMethod.get(ecg_filtration_method,False)

    def did_receive_raw_temperature(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_temperature(data)

    def did_receive_raw_ecg(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_ecg(data)

    def did_receive_raw_respiration(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_respiration(data)
    
    def did_receive_raw_battery_level(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_battery(data)

    def did_receive_raw_imu_values(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_motion(data)

    def did_receive_raw_orientation(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_orientation(data)
    
    def did_receive_raw_steps(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_steps(data)

    def did_receive_raw_activity(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_activity(data)
    
    def did_receive_raw_heart_rate(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_heart_rate(data)

    def did_receive_raw_health_thermometer(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_health_thermometer(data)

    def did_receive_raw_sound_volume(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_sound_volume(data)

    def did_receive_raw_firmware_revision(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].set_firmware_revision(data)
        self.device_information['firmware_revision'] = data

    def did_receive_raw_hardware_revision(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].set_hardware_revision(data)
        self.device_information['hardware_revision'] = data

    def did_receive_raw_manufacture_name(self, data, aidlab_address):
        self.device_information['manufacture_name'] = data

    def did_receive_raw_serial_number(self, data, aidlab_address):
        self.device_information['serial_number'] = data

    #-- Aidlab callbacks -----------------------------------------------

    def did_connect_aidlab(self, aidlab_address):
        pass

    def did_disconnect_aidlab(self, aidlab_address):
        pass

    def push_up_callback(self, aidlab_address):
        pass

    def sit_up_callback(self, aidlab_address):
        pass

    def jump_callback(self, aidlab_address):
        pass

    def burpee_callback(self, aidlab_address):
        pass

    def did_receive_ecg(self, value, timestamp, aidlab_address):
        pass

    def did_receive_activity(self, activity, timestamp, aidlab_address):
        pass

    def did_receive_respiration(self, value, timestamp, aidlab_address):
        pass

    def did_receive_battery_level(self, stateOfCharge, aidlab_address):
        pass

    def did_receive_steps(self, steps, timestamp, aidlab_address):
        pass

    def did_receive_temperature(self, skin_temperature, timestamp, aidlab_address):
        pass

    def did_receive_motion(self, qw, qx, qy, qz, ax, ay, az, timestamp, aidlab_address):
        pass

    def did_receive_orientation(self, roll, pitch, yaw, timestamp, aidlab_address):
        pass

    def did_receive_heart_rate(self, hrv, heartRate, timestamp, aidlab_address):
        pass

    def did_receive_respiration_rate(self, value, timestamp, aidlab_address):
        pass

    def wear_state_did_change(self, state, aidlab_address):
        pass
    
    def did_receive_sound_volume(self, sound_volume, timestamp, aidlab_address):
        pass
    
    
    
 