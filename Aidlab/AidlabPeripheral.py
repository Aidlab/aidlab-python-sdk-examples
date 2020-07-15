#
# Aidlab_peripheral.py
# Aidlab-SDK
# Created by Szymon Gesicki on 10.05.2020.
#

from Aidlab.AidlabCharacteristicsUUID import AidlabCharacteristicsUUID
from Aidlab.AidlabNotificationHandler import AidlabNotificationHandler

from bleak import BleakClient, discover, BleakError
import asyncio
from multiprocessing import Process
import sys


class AidlabPeripheral():
    connected_aidlab = []

    def __init__(self, aidlab_delegate):
        self.aidlab_delegate = aidlab_delegate

    async def scan_for_aidlab(self):

        devices = await discover()
        # Container for Aidlab's MAC addresses (these were found during the scan process)
        aidlabMACs = []

        for dev in devices:
            # Device found with dev.name
            if dev.name == "Aidlab" and dev.address not in self.connected_aidlab:
                aidlabMACs.append(dev.address)
        return aidlabMACs

    def run(self, characteristics, aidlabs_address=None):
        print("Connecting ...")
        loop = asyncio.get_event_loop()
        self.connect(characteristics, loop, aidlabs_address)

    def connect(self, characteristics, loop, aidlabs_address=None):

        # Connect to all Aidlabs from `aidlabsMAC` list
        if aidlabs_address:
            self.create_task(characteristics, aidlabs_address, loop)
            # All Aidlabs connected, end the loop
            return

        # Connect to every discoverable Aidlab
        else:
            while True:
                aidlabs_address = loop.run_until_complete(self.scan_for_aidlab())

                if aidlabs_address != []:
                    self.create_task(characteristics, aidlabs_address, loop)

    def create_task(self, characteristics, aidlabs_address, loop):

        if 'linux' in sys.platform:
            for aidlab_address in aidlabs_address:
                Process(target=self.between, args=(characteristics, aidlab_address, loop)).start()
                self.connected_aidlab.append(aidlab_address)

        elif 'darwin' in sys.platform:
            # unfortunately, macOS does not yet support connection with many devices,
            # so we connect to first Aidlab
            self.between(characteristics, aidlabs_address[0], loop)

        else:
            for aidlab_address in aidlabs_address:
                try:
                    loop.create_task(self.connect_to_aidlab(characteristics, aidlab_address, loop))
                except:
                    pass
                finally:
                    self.connected_aidlab.append(aidlab_address)
            # task to look for more aidlabs
            loop.create_task(self.connect(characteristics, loop))
            loop.run_forever()

    def between(self, characteristics, aidlab_address, loop):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.connect_to_aidlab(characteristics, aidlab_address, loop))
        except:
            pass

    async def connect_to_aidlab(self, characteristics, aidlab_address, loop):

        async with BleakClient(aidlab_address, loop=loop) as client:

            self.aidlab_delegate.create_aidlabSDK(aidlab_address)

            # Harvest Device Information
            self.aidlab_delegate.did_receive_raw_firmware_revision(
                (await client.read_gatt_char("00002a26-0000-1000-8000-00805f9b34fb")).decode('ascii'), aidlab_address)

            self.aidlab_delegate.did_receive_raw_hardware_revision(
                (await client.read_gatt_char("00002a27-0000-1000-8000-00805f9b34fb")).decode('ascii'), aidlab_address)

            self.aidlab_delegate.did_receive_raw_manufacture_name(
                (await client.read_gatt_char("00002a29-0000-1000-8000-00805f9b34fb")).decode('ascii'), aidlab_address)

            self.aidlab_delegate.did_receive_raw_serial_number(
                (await client.read_gatt_char("00002a25-0000-1000-8000-00805f9b34fb")).decode('ascii'), aidlab_address)

            self.aidlab_delegate.did_connect_aidlab(aidlab_address)

            aidlabNotificationHandler = AidlabNotificationHandler(aidlab_address,  self.aidlab_delegate)

            for characteristic in characteristics:
                await client.start_notify(self.converter_to_uuid(characteristic, aidlab_address), aidlabNotificationHandler.handle_notification)

            while True:
                await asyncio.sleep(1, loop=loop)
                if not await client.is_connected():
                    self.aidlab_delegate.did_disconnect_aidlab(aidlab_address)
                    self.aidlab_delegate.destroy(aidlab_address)
                    break

    def converter_to_uuid(self, characteristic, aidlab_address):
        if characteristic == "temperature":
            return AidlabCharacteristicsUUID.temperatureUUID
        elif characteristic == "ecg":
            return AidlabCharacteristicsUUID.ecgUUID
        elif characteristic == "battery":
            return AidlabCharacteristicsUUID.batteryUUID
        elif characteristic == "respiration":
            return AidlabCharacteristicsUUID.respirationUUID
        elif characteristic == "motion":
            return AidlabCharacteristicsUUID.motionUUID
        elif characteristic == "activity":
            return AidlabCharacteristicsUUID.activityUUID
        elif characteristic == "steps":
            return AidlabCharacteristicsUUID.stepsUUID
        elif characteristic == "orientation":
            return AidlabCharacteristicsUUID.orientationUUID
        elif characteristic == "heartRate":
            return AidlabCharacteristicsUUID.heartRateUUID
        elif characteristic == "healthThermometer":
            return AidlabCharacteristicsUUID.health_thermometerUUID
        elif characteristic == "soundVolume":
            return AidlabCharacteristicsUUID.sound_volumeUUID

        print("Signal ", characteristic, " not supported")
        self.aidlab_delegate.did_disconnect_aidlab(aidlab_address)
        exit()
