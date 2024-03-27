#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client import ModbusTcpClient as ModBusClient


class SMA_Modbus:
    '''Base class for SMA Modbeus with TCP
    '''
    def __init__(self, ip, port=502, device_unit_id=3):
        self._client = ModBusClient(ip, port)
        # get Unit ID --> it is at index [3] of results.registers
        #_result = self._client.read_holding_registers(42109, 4, 1)
        #print(type(_result.registers), ": ", _result.registers)
        #self._device_unit = _result.registers[3]
        self._device_unit_id = device_unit_id
        #print("Device Unit: ", self._device_unit_id)
        self.connect()

    def __del__(self):
        self.close()
        del self._device_unit_id
        del self._client

    def connect(self):
        '''Establish conncetion of client
        '''
        try:
            if not self._client.connect():
                print("ERROR: client cannot connect to ModBus-Server!")
            else:
                #print("INFO: client connected successfully to Modbus-Server!")
                pass
        except:
            print("ERROR: Propably an Syntax Error!")
        finally:
            pass

    def close(self):
        '''Close connection of client
        '''
        if self._client.is_socket_open():
            self._client.close()
            #print("INFO: Connection closed!")
        return None

    def read_holding_register(self, register_address, datatype, count = 1):
        '''Read the holding register from SMA device
        '''
        type_to_length = {'U16': 1, 'U32': 2, 'U64': 4, 'S16': 1, 'S32': 2 }
        length = type_to_length[datatype] * count
        #print(f'length : {length}')
        result = self._client.read_holding_registers(register_address, length, slave=self._device_unit_id)
        #print(type(result.registers), ": ", result.registers)
        data = self.decode_register_readings(result, datatype, count)
        return data

    def decode_register_readings(self, readings, datatype, count):
        '''Decode the register readings dependend on datatype
        '''
        decoder = BinaryPayloadDecoder.fromRegisters(readings.registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
        #print(f'decoder : {decoder}')
        if (datatype == 'U16'):
            data = [decoder.decode_16bit_uint() for i in range(count)]
        elif (datatype == 'U32'):
            data = [decoder.decode_32bit_uint() for i in range(count)]
        elif (datatype == 'U64'):
            data = [decoder.decode_64bit_uint() for i in range(count)]
        elif (datatype == 'S16'):
            data = [decoder.decode_16bit_int() for i in range(count)]
        elif (datatype == 'S32'):
            data = [decoder.decode_32bit_int() for i in range(count)]
        return data

    def decode_looping(self, decoder, method, count):
        '''Loop over decoder entries
        '''
        data = [decoder.method() for i in range(count)]
        return data

class Sunnyboy5000TL21(SMA_Modbus):
    '''class for the connection to the SMA SynnyBoy-5000TL-21 by Modbus.
    Make sure the python lib 'pymodbus' is installed
    Please check if the TCP port in the sma device is activated!
    Check Register description --> see specific documentation of manufacturer
    e.g.: http://read.pudn.com/downloads781/ebook/3090423/SMA_Modbus-de-en_V15/SMA_Modbus-TI-de-15.pdf 
    '''

    def get_device_class(self):
        '''Query the device class from register 30051, U32
        '''
        device_class = {8000: 'Alle Geräte', \
                        8001: 'Solar-Wechselrichter', \
                        8002: 'Wind-Wechselrichter', \
                        8007: 'Batterie-Wechselrichter', \
                        8033: 'Verbraucher', \
                        8064: 'Sensorik Allgemein', \
                        8065: 'Stromzähler', \
                        8128: 'Kommunikationsprodukte'}
        data = self.read_holding_register(30051, 'U32')
        class_of_device = device_class[data[0]]
        #print(class_of_device)
        return class_of_device

    def get_device_type(self):
        '''Query device type at register = 30053, U32
        '''
        device_type = {9074: 'SB 3000TL-21', \
                       9075: 'SB 4000TL-21', \
                       9076: 'SB 5000TL-21', \
                       9165: 'SB 3600TL-21'}
        # read device type of default unit id = 3
        data = self.read_holding_register(30053, 'U32')
        Device_Type = device_type[data[0]]
        #print("Device Type: ", Device_Type)
        return Device_Type

    def get_serial_number(self):
        '''Query serial number at register = 30057, U32
        '''
        # read serial number of deafult unit id = 3
        data = self.read_holding_register(30057, 'U32')
        #print("Serial#: ", data)
        return data[0]
    
    def get_software_packet(self):
        '''Get Software Packet at register = 30059;  U32
        '''
        data = self.read_holding_register(30059, 'U32')
        return data[0]

    def get_status_of_device(self):
        '''Query status at register = 30201, U32
        '''
        # read Status of device
        device_status = {35: 'Fehler', 303: 'Aus', 307: 'Ok', 455: 'Warnung'}
        data = self.read_holding_register(30201, 'U32')
        Status = device_status[data[0]]
        #print('Status: ', Status)
        return Status

    def get_grid_relay_status(self):
        '''Derating status of the grid relay/contact at register = 30217; U32
        '''
        relay_status = {51: 'closed', \
                         311: 'open', \
                         16777213: 'information not available'}
        data = self.read_holding_register(30217, 'U32')
        #print(data[0])
        return relay_status[data[0]]

    def get_derating(self):
        '''Derating status of the device at register = 30219; U32
        '''
        derating_code = {557: 'Temperature derating', \
                         884: 'not active', \
                         16777213: 'information not available'}
        data = self.read_holding_register(30219, 'U32')
        #print(data[0])
        return derating_code[data[0]]

    def get_total_yield(self):
        '''Get the total yield at register = 30513; U64
            Total yield in Wh
        '''
        data = self.read_holding_register(30513, 'U64')
        #print(data[0])
        return data[0]

    def get_daily_yield(self):
        '''Get the daily yield at register = 30517; U64
            Total yield in Wh
        '''
        data = self.read_holding_register(30517, 'U64')
        #print(data[0])
        return data[0]

    def get_operating_time(self):
        '''Get operating time at register = 30521; U64
            operating time in s
        '''
        time = self.read_holding_register(30521, 'U64')[0]
        #print(time)
        return time

    def get_feed_in_time(self):
        '''Get feed-in time at register = 30525; U64
            feed-in time in s
        '''
        time = self.read_holding_register(30525, 'U64')[0]
        #print(time)
        return time

    def get_dc_current_in(self):
        '''Get dc current incomming at register = 30769; S32
            DC current in A
        '''
        dc_current = self.read_holding_register(30769, 'S32')[0]
        #print(dc_current)
        if (dc_current < 0):
            dc_current = 0
        return dc_current
    
    def get_dc_voltage_in(self):
        '''Get dc voltage incomming at register = 30771; S32
            DC voltage in V
        '''
        dc_voltage = self.read_holding_register(30769, 'S32')[0]
        #print(dc_voltage)
        if (dc_voltage < 0):
            dc_voltage = 0
        return dc_voltage
    
    def get_dc_power_in(self):
        '''Get dc power incomming at register = 30773; S32
            DC power in W
        '''
        dc_power = self.read_holding_register(30773, 'S32')[0]
        #print(data[0])
        if (dc_power < 0):
            dc_power = 0
        return dc_power
    
    def get_active_power(self):
        '''Getter for the active power of L1, L2, L3
        query Active Power of all at register = 30775, S32
        query Active Power of L1 at register = 30777, S32
        query Active Power of L2 at register = 30779, S32
        query Active Power of L3 at register = 30781, S32
        '''
        data = self.read_holding_register(30775, 'S32', 4)
        #print(type(result.registers), ": ", result.registers)
        P_sum = data[0] / 1000
        if (P_sum < 0):
            P_sum = 0
        P_L1 = data[1]  / 1000
        if (P_L1 < 0):
            P_L1 = 0
        P_L2 = data[2]  / 1000
        if (P_L2 < 0):
            P_L2 = 0
        P_L3 = data[3]  / 1000
        if (P_L3 < 0):
            P_L3 = 0
        #print('Aktive Wirkleistung Summe: ', P_sum, " kW")
        #print('Aktive Wirkleistung L1:\t\t', P_L1, " kW")
        #print('Aktive Wirkleistung L2:\t\t', P_L2, " kW")
        #print('Aktive Wirkleistung L3:\t\t', P_L3, " kW")
        return round(P_sum, 3)

    def get_ac_current(self):
        '''Getter for the actual current of i1, i2, i3
        query AC Current of L1 at register = 30977, S32
        query AC Current of L2 at register = 30979, S32
        query AC Current of L3 at register = 30981, S32
        '''
        # read_holding_registers(Startwert, Anzahl Register, slave=self._device_unit_id)
        data = self.read_holding_register(30977, 'S32', 3)
        I_AC_L1 = data[0] / 1000
        if (I_AC_L1 < 0):
            I_AC_L1 = 0
        I_AC_L2 = data[1] / 1000
        if (I_AC_L2 < 0):
            I_AC_L2 = 0
        I_AC_L3 = data[2] / 1000
        if (I_AC_L3 < 0):
            I_AC_L3 = 0
        #print('AC Strom  L1:\t\t{0:.3f} A'.format(I_AC_L1))
        #print('AC Strom  L2:\t\t{0:.3f} A'.format(I_AC_L2))
        #print('AC Strom  L3:\t\t{0:.3f} A'.format(I_AC_L3))
        return round(I_AC_L1, 3)
