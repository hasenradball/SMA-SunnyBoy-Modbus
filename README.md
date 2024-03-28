# SMA-SunnyBoy-5000TL-21-Modbus
Python solution to connect to the SMA Sunnyboy-5000TL-21.

## Contents
* [Prerecquisites](#prerecquisites)
* [Usage](#usage)
* [License](#license)
* [Helpful Links](#helpful-links)

## Prerecquisites
1) For the use of this python code it is necessary to install the python libs `pymodbus` and `pyserial`:

    `python3 -m pip install pymodbus`
    `python3 -m pip install pyserial`
    
    Remark: use the minimum the version of 3.6.x

2) make sure that your SMA Device supports the modbus protocol
3) make sure that the SMA Device has started/enabled the TCP Server to communicate via modbus

## Usage
Check the python code in the script `sma_modbus.py` and change the settings if necessary.
Then you can check the communucation via:

`python3 sma_modbuy.py`

# License
This library is licensed under MIT Licence.

# Helpful Links
* [ESP8266-01-Adapter](https://esp8266-01-adapter.de)
