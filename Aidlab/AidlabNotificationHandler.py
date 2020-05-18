#
# AidlabNotificationHandler.py
# Aidlab-SDK
# Created by Szymon Gesicki on 09.05.2020.
#

from Aidlab.AidlabCharacteristicsUUID import AidlabCharacteristicsUUID

class AidlabNotificationHandler(object):


    def __init__(self, aidlab_address, delegate):
        self.aidlab_address = aidlab_address
        self.delegate = delegate

    def handle_notification(self, sender, data):
        
        if sender == AidlabCharacteristicsUUID.temperatureUUID or sender == AidlabCharacteristicsUUID.temperatureUUID.upper():
            self.delegate.did_receive_raw_temperature(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.ecgUUID or sender == AidlabCharacteristicsUUID.ecgUUID.upper():
            self.delegate.did_receive_raw_ecg(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.batteryUUID or sender == AidlabCharacteristicsUUID.batteryUUID.upper():
            self.delegate.did_receive_raw_battery_level(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.respirationUUID or sender == AidlabCharacteristicsUUID.respirationUUID.upper():
            self.delegate.did_receive_raw_respiration(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.motionUUID or sender == AidlabCharacteristicsUUID.motionUUID.upper():
            self.delegate.did_receive_raw_imu_values(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.activityUUID or sender == AidlabCharacteristicsUUID.activityUUID.upper():
            self.delegate.did_receive_raw_activity(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.stepsUUID or sender == AidlabCharacteristicsUUID.stepsUUID.upper():
            self.delegate.did_receive_raw_steps(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.orientationUUID or sender == AidlabCharacteristicsUUID.orientationUUID.upper():
            self.delegate.did_receive_raw_orientation(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.heartRateUUID or sender == AidlabCharacteristicsUUID.heartRateUUID.upper():
            self.delegate.did_receive_raw_heart_rate(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.health_thermometerUUID or sender == AidlabCharacteristicsUUID.health_thermometerUUID.upper():
            self.delegate.did_receive_raw_health_thermometer(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.sound_volumeUUID or sender == AidlabCharacteristicsUUID.sound_volumeUUID.upper():
            self.delegate.did_receive_raw_sound_volume(data, self.aidlab_address)

    