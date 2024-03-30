# SMA-SunnyBoy-Modbus
Python solution connecting the SMA Sunnyboy inverters.

![SMA-SunnyBoy](./docs/SMA/SMA-SunnyBoy.jpg)

## Contents
* [Prerecquisites](#prerecquisites)
* [Usage](#usage)
* [License](#license)
* [Helpful Links](#helpful-links)

## Prerecquisites
1) For the use of this python code it is necessary to install the python libs `pymodbus` and `pyserial`:

    python3 -m pip install pymodbus<br>
    python3 -m pip install pyserial
    
    Remark: for `pymodbus` use the minimum version of 3.6.x

2) make sure that your SMA Device supports the modbus protocol
3) make sure that the SMA Device has started/enabled the TCP Server to communicate via modbus

## Usage
Check the python code in the script `sma_modbus.py` and change the settings if necessary.
Especially the ip-address has to be adapted to your settings in the following line:
    
     sunny_obj = sunny_boy("192.168.xxx.xxx")

Alternativly you can instanciate the object with the device UnitID by:

    sunny_obj = sunny_boy("192.168.xxx.xxx", UnitID)

Normally the device UnitID is `3` as default. If not sure you can use the funtion `read_device_unit_id()`.

    sunny_obj = sunny_boy("192.168.178.29")
    print(sunny_obj.read_device_unit_id())

Then you can check the communucation via:

    python3 sma_modbus.py

# License
This library is licensed under MIT Licence.

# Helpful Links
* [ESP8266-01-Adapter](https://esp8266-01-adapter.de)
