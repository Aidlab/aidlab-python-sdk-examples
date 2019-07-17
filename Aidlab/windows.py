#
# windows.py
# Aidlab-SDK
# Created by S Gęsicki on 01.07.2019.
#
from bleak import BleakClient, discover, BleakError
from .data import calculate_ecg, calculate_motion, calculate_respiration, calculate_temperature, calculate_battery, initial, get_analyse
from multiprocessing import Process, Queue
import uuid
from ctypes import CFUNCTYPE
import asyncio

temperatureUUID = "45366e80-cf3a-11e1-9ab4-0002a5d5c51b"
ecgUUID = "46366e80-cf3a-11e1-9ab4-0002a5d5c51b"
respirationUUID = "48366e80-cf3a-11e1-9ab4-0002a5d5c51b"
batteryUUID = "47366e80-cf3a-11e1-9ab4-0002a5d5c51b"
motionUUID = "49366e80-cf3a-11e1-9ab4-0002a5d5c51b"
connected_aidlab = []


class Aidlab(object):
    def __init__(self):
        self.heartRate = -1
        self.respirationRate = -1


class Status():
    def __init__(self, status, address):
        self.status = status
        self.address = address


class NotificationHandler():

    def __init__(self, aidlab):
        self.aidlab = aidlab
        self.counter = 0

    def handleNotification(self, sender, data):
        self.counter = get_analyse(self.aidlab, self.counter)
        if sender == temperatureUUID:
            self.callback(self.aidlab, "temperature",
                          calculate_temperature(data))
        elif sender == ecgUUID:
            self.callback(self.aidlab, "ecg", calculate_ecg(data))
        elif sender == batteryUUID:
            self.callback(self.aidlab, "battery", calculate_battery(data))
        elif sender == respirationUUID:
            self.callback(self.aidlab, "respiration",
                          calculate_respiration(data))
        elif sender == motionUUID:
            self.callback(self.aidlab, "motion", calculate_motion(data))


class AidlabManager():

    async def scan_for_aidlab(self):
        global connected_aidlab
        devices = await discover()

        aidlabMACs = []
        # Container for Aidlab's MAC addresses (these were found during the scan process)
        for dev in devices:
            if dev.name == "Aidlab" and dev.address not in connected_aidlab:  # Device found with dev.name
                aidlabMACs.append(dev.address)
        return aidlabMACs

    def connect(self, characteristics, aidlabsMAC=None):

        loop = asyncio.get_event_loop()
        global connected_aidlab
        q = Queue()
        print("Connecting ...")

        if aidlabsMAC:  # Connect to all Aidlabs from `aidlabsMAC` list
            number_of_aidlabs = len(aidlabsMAC)
            # All Aidlabs connected, end the loop
            while number_of_aidlabs != len(connected_aidlab):
                for aidlabMAC in aidlabsMAC:
                    self.__make_new_process(characteristics, aidlabMAC, q)
                    aidlabsMAC.remove(aidlabMAC)
                while not q.empty():
                    status = q.get()
                    if status.status:
                        connected_aidlab.append(status.address)
                    else:
                        aidlabsMAC.append(status.address)
        else:  # Connect to every discoverable Aidlab
            while True:
                aidlabsMAC = loop.run_until_complete(self.scan_for_aidlab())
                for aidlabMAC in aidlabsMAC:
                    self.__make_new_process(characteristics, aidlabMAC, q)
                    connected_aidlab.append(aidlabMAC)
                while not q.empty():
                    status = q.get()
                    if not status.status:
                        connected_aidlab.remove(status.address)
                aidlabsMAC = None

    # every new aidlab is a new process, because if we will get out of the loop connect_to_aidlab, the bleak lib will stop notifying.
    def __make_new_process(self, characteristics, aidlabMAC, q):
        notificationhandler = NotificationHandler(Aidlab())
        notificationhandler.callback = self.data_receiver
        Process(target=self.between, args=(notificationhandler,
                                           characteristics, aidlabMAC, q)).start()

    def between(self, notificationhandler, characteristics, aidlabMACaddress, q):
        # initial python_sdk lib because it has to be in process

        initial(self.pushup_callback, self.situp_callback, self.jump_callback)

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.__connect_to_aidlab(
                notificationhandler, characteristics, aidlabMACaddress, loop, q, True))
        except BleakError:
            q.put(Status(False, aidlabMACaddress))
        except:
            pass

    async def __connect_to_aidlab(self, notificationhandler, characteristics, aidlabMACAddress, loop, q, debug=False):
        async with BleakClient(aidlabMACAddress, loop=loop) as client:
            q.put(Status(True, aidlabMACAddress))
            self.is_connected(aidlabMACAddress)

            # Harvest Device Information
            deviceInformation = {
                "serialNumber": (await client.read_gatt_char(uuid.UUID("00002a25-0000-1000-8000-00805f9b34fb"))).decode(
                    'ascii'),
                "firmwareRevision": (await client.read_gatt_char(uuid.UUID("00002a26-0000-1000-8000-00805f9b34fb"))).decode(
                    'ascii'),
                "hardwareRevision": (await client.read_gatt_char(uuid.UUID("00002a27-0000-1000-8000-00805f9b34fb"))).decode(
                    'ascii'),
                "manufacturerName": (await client.read_gatt_char(uuid.UUID("00002a29-0000-1000-8000-00805f9b34fb"))).decode(
                    'ascii')}

            notificationhandler.aidlab.address = aidlabMACAddress
            notificationhandler.aidlab.deviceInformation = deviceInformation

            for characteristic in characteristics:
                await client.start_notify(self.__converter_to_uuid(characteristic, notificationhandler.aidlab), notificationhandler.handleNotification)

            while True:
                await asyncio.sleep(1, loop=loop)
                if not await client.is_connected():
                    self.is_disconnected(notificationhandler.aidlab)
                    break

    def __converter_to_uuid(self, characteristic, aidlab):
        if characteristic == "temperature":
            return uuid.UUID(temperatureUUID)
        elif characteristic == "ecg":
            return uuid.UUID(ecgUUID)
        elif characteristic == "battery":
            return uuid.UUID(batteryUUID)
        elif characteristic == "respiration":
            return uuid.UUID(respirationUUID)
        elif characteristic == "motion":
            return uuid.UUID(motionUUID)

        print("Characteristic ", characteristic, " not supported")
        self.is_disconnected(aidlab)
        exit()

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
