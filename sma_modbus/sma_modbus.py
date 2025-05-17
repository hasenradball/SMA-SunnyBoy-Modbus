"""Class for SMA Modbus Connection"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymodbus.client import ModbusTcpClient as ModBusClient
from pymodbus import (FramerType, ExceptionResponse, ModbusException)
from .modbus_constants import ModbusConstants as CONSTS


class SmaModbus:
    """Base class for SMA Modbeus with TCP
    """
    def __init__(self, ip, port = 502, device_unit_id = 3):
        """Constructor of modbus object
        
        Keyword arguments:

        ip -- ip address of device

        port -- port of device (default 502)

        device_unit_id -- UnitID (default 3)

        """
        self._client = ModBusClient(ip, port=port, framer=FramerType.SOCKET)
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
        readings = self._client.read_holding_registers(42109, count=4, slave=1)
        unit_id = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.UINT16)[3]
        #print(f'UnitID       : {unit_id}')
        return unit_id

    def connect(self):
        """Establish connection of client
        """
        try:
            if not self._client.connect():
                print("ERROR: client cannot connect to ModBus-Server!")
            else:
                #print("INFO: client connected successfully to Modbus-Server!")
                pass
        except Exception as exc:
            print(f"ERROR: received an exception {exc}! Probably an Syntax Error!")
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
        try:
            result = self._client.read_holding_registers(register_address, \
                count=length, slave=self._device_unit_id)
            #print(result, type(result))
        except ModbusException as exc:
            print(f">>> read_holding_register: Received ModbusException({exc}) from library")
        if result.isError():
            print(f">>> read_holding_register: Received Modbus library error({result})")
        if isinstance(result, ExceptionResponse):
            print(f">>> read_holding_register: Received Modbus library exception ({result})")
            # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
            return False
        #print(type(result.registers), ": ", result.registers)
        data = self.decode_register_readings(result, datatype, count)
        return data

    def decode_register_readings(self, readings, datatype, count):
        """Decode the register readings depend on datatype

        Keyword arguments:

        readings -- register readings to decode

        datatype -- U8, U16, U32, etc...

        count -- number of datatypes to decode
        
        --
        """
        data = []
        if datatype == 'U16':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.UINT16)
        elif datatype == 'U32':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.UINT32)
        elif datatype == 'U64':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.UINT64)
        elif datatype == 'S16':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.INT16)
        elif datatype == 'S32':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.INT32)
        elif datatype == 'S64':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.INT64)
        return data


class SunnyBoy(SmaModbus):
    """class for the connection to the SMA SunnyBoy by Modbus.
    
    Make sure the python lib 'pymodbus' is installed
    Please check if the TCP port in the sma device is activated!
    Check Register description --> see specific documentation of manufacturer 
    """

    def get_device_class(self) -> str:
        """Read the device class
        
        -----
        Returns:
            device class if successful, False otherwise
        -----
        Register address: 30051; U32
        Function-Code: 0x04
        Unit: -
        """
        data = self.read_holding_register(30051, 'U32')
        class_of_device = CONSTS.DEVICE_CLASS[data]
        #print(class_of_device)
        return class_of_device

    def get_device_type(self) -> str:
        """Read the device type
        
        -----
        Returns:
            device type if successful, False otherwise
        -----
        Register address: 30053; U32
        Function-Code: 0x04
        Unit: -
        """

        # read device type of default unit id = 3
        data = self.read_holding_register(30053, 'U32')
        device = CONSTS.DEVICE_TYPE[data]
        #print("Device Type: ", Device_Type)
        return device

    def get_serial_number(self) -> int :
        """Read the serial number
        
        -----
        Returns:
            serial number if successful, False otherwise
        -----
        Register address: 30057; U32
        Function-Code: 0x04
        Unit: -
        """
        # read serial number of default unit id = 3
        data = self.read_holding_register(30057, 'U32')
        #print("Serial#: ", data)
        return data

    def get_software_packet(self) -> int :
        """Read the software packet information
        
        -----
        Returns:
            software packet information if successful, False otherwise
        -----
        Register address: 30059; U32
        Function-Code: 0x04
        Unit: -
        """
        data = self.read_holding_register(30059, 'U32')
        return data

    def get_status_of_device(self) -> str:
        """Read the device status
        
        -----
        Returns:
            status of device if successful, False otherwise
        -----
        Register address: 30201; U32
        Function-Code: 0x04
        Unit: -
        """
        data = self.read_holding_register(30201, 'U32')
        status = CONSTS.DEVICE_STATUS[data]
        #print('Status: ', Status)
        return status

    def get_grid_relay_status(self) -> str:
        """Read the status of the grid relay/contact
        
        Register: 30217; U32
        -----
        Returns:
            status of grid contact if successful, False otherwise
        -----
        Register address: 30217; U32
        Function-Code: 0x04
        Unit: -
        """
        data = self.read_holding_register(30217, 'U32')
        #print(data)
        return CONSTS.RELAY_STATE[data]

    def get_derating(self) -> str:
        """Read the derating state of the device 
        
        Register: 30219; U32
        -----
        Returns:
            derating state if successful, False otherwise
        -----
        Register address: 30219; U32
        Function-Code: 0x04
        Unit: -
        """
        data = self.read_holding_register(30219, 'U32')
        #print(data)
        return CONSTS.DERATING_STATE[data]

    def get_total_yield(self) -> int:
        """Read the total yield
        
        get the total yield in Wh
        -----
        Returns:
            total yield if successful, False otherwise
        -----
        Register address: 30513; U64
        Function-Code: 0x04
        Unit: Wh
        """
        data = self.read_holding_register(30513, 'U64')
        #print(data)
        return data

    def get_daily_yield(self) -> int:
        """Read the daily yield
        
        get daily yield in Wh
        -----
        Returns:
            daily yield if successful, False otherwise
        -----
        Register address: 30517; U64
        Function-Code: 0x04
        Unit: Wh
        """
        data = self.read_holding_register(30517, 'U64')
        #print(data)
        return data

    def get_operating_time(self) -> int:
        """Read the operating time
        
        get the operating time in seconds
        -----
        Returns:
            time in seconds if successful, False otherwise
        -----
        Register address: 30521; U64
        Function-Code: 0x04
        Unit: s
        """
        time = self.read_holding_register(30521, 'U64')
        #print(time)
        return time

    def get_feed_in_time(self) -> int:
        """Read the feed-in time
        
        get the feed in time in seconds
        -----
        Returns:
            feed in time in seconds if successful, False otherwise
        -----
        Register address: 30525; U64
        Function-Code: 0x04
        Unit: s
        """
        time = self.read_holding_register(30525, 'U64')
        #print(time)
        return time

    def get_dc_current_in(self) -> float:
        """Read the incoming dc current
        
        get DC current incoming
        -----
        Returns:
            dc current if successful, False otherwise
        -----
        Register address: 30769; S32
        Function-Code: 0x04
        Unit: A
        """
        dc_current = self.read_holding_register(30769, 'S32')/1000
        #print(dc_current)
        if dc_current < 0:
            dc_current = 0
        return dc_current

    def get_dc_voltage_in(self) -> float:
        """Read the incoming dc voltage
        
        get DC voltage incoming
        -----
        Returns:
            DC voltage if successful, False otherwise
        -----
        Register address: 30771; S32
        Function-Code: 0x04
        Unit: V
        """
        dc_voltage = self.read_holding_register(30771, 'S32')/100
        #print(dc_voltage)
        if dc_voltage < 0:
            dc_voltage = 0
        return dc_voltage

    def get_dc_power_in(self):
        """Read the incoming dc power
            
        get the DC power incoming
        -----
        Returns:
            dc power if successful, False otherwise
        -----
        Register address: 30773; S32
        Function-Code: 0x04
        Unit: W
        """
        dc_power = self.read_holding_register(30773, 'S32')
        #print(dc_power)
        if dc_power < 0:
            dc_power = 0
        return dc_power

    def get_active_power(self) -> tuple:
        """Read the active power of phases L1, L2, L3

        Active Power of all phases
        Register: 30775; S32
        ----
        Active Power of L1 phase
        Register: 30777; S32
        ----
        Active Power of L2 phase
        Register: 30779; S32
        ----
        Active Power of L3 phase
        Register: 30781; S32
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

    def get_ac_current(self) -> tuple:
        """Read the actual current of phases i1, i2, i3
        
        AC Current of L1
        Register: 30977; S32
        ----
        AC Current of L2
        Register: 30979; S32
        ----
        AC Current of L3
        Register: 30981; S32
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
