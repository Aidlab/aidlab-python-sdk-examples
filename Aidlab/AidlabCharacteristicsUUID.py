#
# AidlabCharacteristicsUUID.py
# Aidlab-SDK
# Created by Szymon Gesicki on 10.05.2020.
#

import sys

class AidlabCharacteristicsUUID:

    temperatureUUID =        "45366e80-cf3a-11e1-9ab4-0002a5d5c51b"
    ecgUUID =                "46366e80-cf3a-11e1-9ab4-0002a5d5c51b"
    batteryUUID =            "47366e80-cf3a-11e1-9ab4-0002a5d5c51b"
    respirationUUID =        "48366e80-cf3a-11e1-9ab4-0002a5d5c51b"
    motionUUID =             "49366e80-cf3a-11e1-9ab4-0002a5d5c51b"
    activityUUID =           "61366e80-cf3a-11e1-9ab4-0002a5d5c51b"
    stepsUUID =              "62366e80-cf3a-11e1-9ab4-0002a5d5c51b"
    orientationUUID =        "63366e80-cf3a-11e1-9ab4-0002a5d5c51b"
    sound_volumeUUID =       "52366e80-cf3a-11e1-9ab4-0002a5d5c51b"
    heartRateUUID =          "2a37" if 'darwin' in sys.platform else "00002a37-0000-1000-8000-00805f9b34fb"
    health_thermometerUUID = "2a1c" if 'darwin' in sys.platform else "00002a1c-0000-1000-8000-00805f9b34fb"