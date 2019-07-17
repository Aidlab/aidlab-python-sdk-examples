from time import sleep
import time
from ctypes import CFUNCTYPE
from pyble.handlers import PeripheralHandler, ProfileHandler
from .data import calculate_ecg, calculate_motion, calculate_respiration, calculate_temperature, calculate_battery, initial, get_analyse
import pyble
import uuid
import sys

# Disable logging
import logging
logging.disable(sys.maxsize)
sys.dont_write_bytecode = True


class DeviceInformationService(ProfileHandler):
    UUID = "180A"
    _AUTOLOAD = True
    names = {
        "2A25": "Serial Number String Characteristic",
        "2A26": "Firmware Revision String Characteristic",
        "2A27": "Hardware Revision String Characteristic",
        "2A29": "Manufacturer Name String Characteristic"
    }

    def initialize(self):
        pass


class UserService(ProfileHandler):
    UUID = "44366E80-CF3A-11E1-9AB4-0002A5D5C51B"
    _AUTOLOAD = True
    names = {
        "45366E80-CF3A-11E1-9AB4-0002A5D5C51B": "Temperature Characteristic",
        "46366E80-CF3A-11E1-9AB4-0002A5D5C51B": "ECG Characteristic",
        "47366E80-CF3A-11E1-9AB4-0002A5D5C51B": "Battery Characteristic",
        "48366E80-CF3A-11E1-9AB4-0002A5D5C51B": "Respiration Characteristic",
        "49366E80-CF3A-11E1-9AB4-0002A5D5C51B": "Motion Characteristic"
    }

    def initialize(self):
        pass

    def on_notify(self, characteristic, data):
        if hasattr(characteristic.service.peripheral, 'deviceInformation'):
            aidlab = characteristic.service.peripheral

            # Copy UUID to address, to match the Linux API
            aidlab.address = characteristic.service.peripheral.UUID

            if characteristic.UUID == "45366E80-CF3A-11E1-9AB4-0002A5D5C51B":
                temperature = calculate_temperature(data)
                _callback(aidlab, "temperature", temperature)
            elif characteristic.UUID == "46366E80-CF3A-11E1-9AB4-0002A5D5C51B":
                ecg = calculate_ecg(data)
                _callback(aidlab, "ecg", ecg)
            elif characteristic.UUID == "47366E80-CF3A-11E1-9AB4-0002A5D5C51B":
                battery = calculate_battery(data)
                _callback(aidlab, "battery", battery)

            elif characteristic.UUID == "48366E80-CF3A-11E1-9AB4-0002A5D5C51B":
                respiration = calculate_respiration(data)
                _callback(aidlab, "respiration", respiration)

            elif characteristic.UUID == "49366E80-CF3A-11E1-9AB4-0002A5D5C51B":
                motion = calculate_motion(data)
                _callback(aidlab, "motion", motion)


class AidlabPeripheral(PeripheralHandler):

    def initialize(self):
        self.addProfileHandler(UserService)
        self.addProfileHandler(DeviceInformationService)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_rssi(self, value):
        pass


class AidlabManager(object):

    def __connect_to_aidlab(self, cm, target):
        target.delegate = AidlabPeripheral
        self.is_connected(target)
        return cm.connectPeripheral(target)

    def __init_peripheral(self, p, characteristics):
        # Harvest Device Information
        deviceInformation = {
            "serialNumber": p["180A"]["2A25"].value,
            "firmwareRevision": p["180A"]["2A26"].value,
            "hardwareRevision": p["180A"]["2A27"].value,
            "manufacturerName": p["180A"]["2A29"].value
        }

        # Store Device Information within peripheral
        p.deviceInformation = deviceInformation
        # Sometimes it takes a while before `notify` will work
        for characteristic in characteristics:
            if characteristic == "temperature":
                p["44366E80-CF3A-11E1-9AB4-0002A5D5C51B"]["45366E80-CF3A-11E1-9AB4-0002A5D5C51B"].notify = True
            elif characteristic == "ecg":
                p["44366E80-CF3A-11E1-9AB4-0002A5D5C51B"]["46366E80-CF3A-11E1-9AB4-0002A5D5C51B"].notify = True
            elif characteristic == "respiration":
                p["44366E80-CF3A-11E1-9AB4-0002A5D5C51B"]["48366E80-CF3A-11E1-9AB4-0002A5D5C51B"].notify = True
            elif characteristic == "battery":
                p["44366E80-CF3A-11E1-9AB4-0002A5D5C51B"]["47366E80-CF3A-11E1-9AB4-0002A5D5C51B"].notify = True
            elif characteristic == "motion":
                p["44366E80-CF3A-11E1-9AB4-0002A5D5C51B"]["49366E80-CF3A-11E1-9AB4-0002A5D5C51B"].notify = True
            else:
                print("Characteristic {} not supported".format(characteristic))

    def connect(self, characteristics, aidlabUUIDs=None):
        global _callback
        _callback = self.data_receiver
        # initial python_sdk
        initial(self.pushup_callback, self.situp_callback, self.jump_callback)

        # Init Central Manager
        cm = pyble.CentralManager()
        if not cm.ready:
            print("Central Manager not ready")
            return

        print("Connecting ...")

        target = None

        if aidlabUUIDs:  # Connect to all Aidlabs from `aidlabUUIDs` list

            # Map aidlabUUIDs string to Python's UUID
            uuids = []
            for aidlabUUID in aidlabUUIDs:
                print(aidlabUUID)
                uuids.append(uuid.UUID("{"+aidlabUUID+"}"))

            peripherals = []

            # Iterate till we will connect with all Aidlabs from the list
            while True:
                target = cm.startScan()
                if target and target.UUID in uuids:

                    # We don't that UUID any longer
                    uuids.remove(target.UUID)

                    # We have to subscribe to Aidlab's characteristics a bit later,
                    # otherwise scanner might get locked
                    p = self.__connect_to_aidlab(cm, target)
                    peripherals.append(p)

                    # Log how many Aidlab left to connect
                    connected_count = len(aidlabUUIDs) - len(uuids)
                    print(
                        "Connection [{}/{}]".format(connected_count, len(aidlabUUIDs)))

                    # All Aidlabs connected, end the loop
                    if len(uuids) == 0:
                        break

            # Connect to saved targets (Aidlabs)
            for p in peripherals:
                self.__init_peripheral(p, characteristics)

            cm.loop()

        else:  # Connect to every discoverable Aidlab
            while True:
                try:
                    target = cm.startScan()
                    if target and target.name == "Aidlab":
                        p = self.__connect_to_aidlab(cm, target)
                        self.__init_peripheral(p, characteristics)
                except Exception as e:
                    print(e)

    def data_receiver(self, aidlab, characteristic_name, data):
        pass

    def is_connected(self, address):
        pass

    def is_disconnected(self, aidlab):
        pass

    @CFUNCTYPE(None)
    def pushup_callback():
        pass

    @CFUNCTYPE(None)
    def jump_callback():
        pass

    @CFUNCTYPE(None)
    def situp_callback():
        pass
