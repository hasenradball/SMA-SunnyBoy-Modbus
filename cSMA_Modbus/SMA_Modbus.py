"""Class for SMA Modbus Connection"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client import ModbusTcpClient as ModBusClient
from .Modbus_Constants import ModbusConstants as CONSTS


class SMA_Modbus:
    """Base class for SMA Modbeus with TCP
    """
    def __init__(self, ip, port = 502, device_unit_id = 3):
        """Constuctor of modbus object
        
        Keyword arguments:

        ip -- ip address of device

        port -- port of device (default 502)

        device_unit_id -- UnitID (default 3)

        """
        self._client = ModBusClient(ip, port)
        # read the device unit id if not sure
        #self.read_device_unit_id()
        self._device_unit_id = device_unit_id
        #print("Device Unit: ", self._device_unit_id)
        self.connect()

    def __del__(self):
        self.close()
        del self._device_unit_id
        del self._client

    def read_device_unit_id(self):
        """Read the device unit id
        
        Read via holding regigster (0x03) and the unit ID the following data:
            - physical serialnumer (2 registers)
            - physical SusyID (1 register)
            - device unit ID (1 register); 3...123; default = 3
        ---
        Register: 42109; U32, U16, U16
        """
        readings = self._client.read_holding_registers(42109, 4, slave=1)
        #print(readings.registers)
        decoder = BinaryPayloadDecoder.fromRegisters(readings.registers, \
                byteorder=Endian.BIG, wordorder=Endian.BIG)
        physical_serial_number = decoder.decode_32bit_uint()
        physical_susy_id = decoder.decode_16bit_uint()
        unit_id = decoder.decode_16bit_uint()
        #print(f'serial number: #{physical_serial_number}')
        #print(f'SusyID       : {physical_susy_id}')
        #print(f'UnitID       : {unit_id}')
        return unit_id

    def connect(self):
        """Establish conncetion of client
        """
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
        """Close connection of client
        """
        if self._client.is_socket_open():
            self._client.close()
            #print("INFO: Connection closed!")
        return None

    def read_holding_register(self, register_address, datatype, count = 1):
        """Read the holding register from SMA device

        Keyword arguments:

        register_address -- number of register address

        datatype -- U8, U16, U32, etc...

        count -- number of datatypes to read (default 1)
        
        --
        Function code : 0x03
        """
        length = CONSTS.TYPE_TO_LENGTH[datatype] * count
        #print(f'length : {length}')
        result = self._client.read_holding_registers(register_address, \
                length, slave=self._device_unit_id)
        #print(type(result.registers), ": ", result.registers)
        data = self.decode_register_readings(result, datatype, count)
        return data

    def decode_register_readings(self, readings, datatype, count):
        """Decode the register readings dependend on datatype

        Keyword arguments:

        readings -- register readings to decode

        datatype -- U8, U16, U32, etc...

        count -- number of datatypes to decode
        
        --
        """
        decoder = BinaryPayloadDecoder.fromRegisters(readings.registers, \
                byteorder=Endian.BIG, wordorder=Endian.BIG)
        #print(f'decoder : {decoder}')
        if datatype == 'U8':
            data = [decoder.decode_8bit_uint() for i in range(count)]
        elif datatype == 'U16':
            data = [decoder.decode_16bit_uint() for i in range(count)]
        elif datatype == 'U32':
            data = [decoder.decode_32bit_uint() for i in range(count)]
        elif datatype == 'U64':
            data = [decoder.decode_64bit_uint() for i in range(count)]
        elif datatype == 'S8':
            data = [decoder.decode_16bit_int() for i in range(count)]
        elif datatype == 'S16':
            data = [decoder.decode_8bit_int() for i in range(count)]
        elif datatype == 'S32':
            data = [decoder.decode_32bit_int() for i in range(count)]
        elif datatype == 'S64':
            data = [decoder.decode_64bit_int() for i in range(count)]
        return data


class SunnyBoy(SMA_Modbus):
    """class for the connection to the SMA SunnyBoy by Modbus.
    
    Make sure the python lib 'pymodbus' is installed
    Please check if the TCP port in the sma device is activated!
    Check Register description --> see specific documentation of manufacturer 
    """

    def get_device_class(self):
        """Read the device class
        
        Register: 30051, U32
        """
        data = self.read_holding_register(30051, 'U32')
        class_of_device = CONSTS.DEVICE_CLASS[data[0]]
        #print(class_of_device)
        return class_of_device

    def get_device_type(self):
        """Read the device type
        
        Register: 30053, U32
        """

        # read device type of default unit id = 3
        data = self.read_holding_register(30053, 'U32')
        device = CONSTS.DEVICE_TYPE[data[0]]
        #print("Device Type: ", Device_Type)
        return device

    def get_serial_number(self):
        """Read the serial number
        
        Register: 30057, U32
        """
        # read serial number of deafult unit id = 3
        data = self.read_holding_register(30057, 'U32')
        #print("Serial#: ", data)
        return data[0]

    def get_software_packet(self):
        """Read the software packet information
        
        Register: 30059;  U32
        """
        data = self.read_holding_register(30059, 'U32')[0]
        return data

    def get_status_of_device(self):
        """Read the device status
        
        Register: 30201, U32
        """
        data = self.read_holding_register(30201, 'U32')[0]
        status = CONSTS.DEVICE_STATUS[data]
        #print('Status: ', Status)
        return status

    def get_grid_relay_status(self):
        """Read the status of the grid relay/contact
        
        Register: 30217; U32
        """

        data = self.read_holding_register(30217, 'U32')[0]
        #print(data[0])
        return CONSTS.RELAY_STATE[data]

    def get_derating(self):
        """Read the derating state of the device 
        
        Register: 30219; U32
        """
        data = self.read_holding_register(30219, 'U32')[0]
        #print(data[0])
        return CONSTS.DERATING_CODE[data]

    def get_total_yield(self):
        """Read the total yield
        
        Total yield
        Register: 30513; U64
        Unit: Wh
        """
        data = self.read_holding_register(30513, 'U64')
        #print(data[0])
        return data[0]

    def get_daily_yield(self):
        """Read the daily yield
        
        Total yield
        Register: 30517; U64
        Unit: Wh
        """
        data = self.read_holding_register(30517, 'U64')[0]
        #print(data)
        return data

    def get_operating_time(self):
        """Read the operating time
        
        Operating time
        Register: 30521; U64
        Unit: s
        """
        time = self.read_holding_register(30521, 'U64')[0]
        #print(time)
        return time

    def get_feed_in_time(self):
        """Read the feed-in time
        
        feed-in time
        Register: 30525; U64
        Unit: s
        """
        time = self.read_holding_register(30525, 'U64')[0]
        #print(time)
        return time

    def get_dc_current_in(self):
        """Read the incomming dc current
        
        DC current incomming
        Register: 30769; S32
        Unit: A
        """
        dc_current = self.read_holding_register(30769, 'S32')[0]/1000
        #print(dc_current)
        if dc_current < 0:
            dc_current = 0
        return dc_current

    def get_dc_voltage_in(self):
        """Read the incommng dc voltage incomming
        
        DC voltage incomming
        Register: 30771; S32
        Unit: V
        """
        dc_voltage = self.read_holding_register(30771, 'S32')[0]/100
        #print(dc_voltage)
        if dc_voltage < 0:
            dc_voltage = 0
        return dc_voltage

    def get_dc_power_in(self):
        """Read the incomming dc power incomming
            
        DC power incomming
        Register: 30773; S32
        Unit: W
        """
        dc_power = self.read_holding_register(30773, 'S32')[0]
        #print(data[0])
        if dc_power < 0:
            dc_power = 0
        return dc_power

    def get_active_power(self):
        """Read the active power of phases L1, L2, L3

        Active Power of all phases
        Register: 30775, S32
        ----
        Active Power of L1 phase
        Register: 30777, S32
        ----
        Active Power of L2 phase
        Register: 30779, S32
        ----
        Active Power of L3 phase
        Register: 30781, S32
        ----
        Unit: kW
        """
        data = self.read_holding_register(30775, 'S32', 4)
        #print(type(result.registers), ": ", result.registers)
        p_sum = round(data[0] / 1000, 3)
        if p_sum < 0:
            p_sum = 0
        p1 = round(data[1]  / 1000, 3)
        if p1 < 0:
            p1 = 0
        p2 = round(data[2]  / 1000, 3)
        if p2 < 0:
            p2 = 0
        p3 = round(data[3]  / 1000, 3)
        if p3 < 0:
            p3 = 0
        #print('Aktive Wirkleistung Summe: ', p_sum, " kW")
        #print('Aktive Wirkleistung L1:\t\t', p1, " kW")
        #print('Aktive Wirkleistung L2:\t\t', p2, " kW")
        #print('Aktive Wirkleistung L3:\t\t', p3, " kW")
        return (p_sum, p1, p2, p3)

    def get_ac_current(self):
        """Read the actual current of phases i1, i2, i3
        
        AC Current of L1
        Register: 30977, S32
        ----
        AC Current of L2
        Register: 30979, S32
        ----
        AC Current of L3
        Register: 30981, S32
        ----
        Unit: A
        """
        # read_holding_registers(Startwert, Anzahl Register, slave=self._device_unit_id)
        data = self.read_holding_register(30977, 'S32', 3)
        i1_ac = round(data[0] / 1000, 3)
        if i1_ac < 0:
            i1_ac = 0
        i2_ac = round(data[1] / 1000, 3)
        if i2_ac < 0:
            i2_ac = 0
        i3_ac = round(data[2] / 1000, 3)
        if i3_ac < 0:
            i3_ac = 0
        #print('AC Strom  L1:\t\t{0:.3f} A'.format(i_ac_L1))
        #print('AC Strom  L2:\t\t{0:.3f} A'.format(i_ac_L2))
        #print('AC Strom  L3:\t\t{0:.3f} A'.format(i_ac_L3))
        return (i1_ac, i2_ac, i3_ac)
