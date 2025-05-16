# SMA-SunnyBoy-Modbus
Python solution connecting the SMA Sunnyboy inverters.

![SMA-SunnyBoy](./docs/SMA/SMA-SunnyBoy.jpg)

## Contents
* [Prerecquisites](#prerecquisites)
* [Installation Steps](#installation-steps)
* [Library Installation](#library-installation)
* [Library Usage](#library-usage)
* [License](#license)
* [Helpful Links](#helpful-links)

## Prerecquisites
1. For this library you need python3
2. For the use of this python code it is necessary to install the python libs:
    - `pymodbus v3.9.2`
    - `pyserial`
> Remark: for `pymodbus` use the minimum version of 3.9.x, testetd with pymodbus==3.9.2

## Installation steps
### Make python ready to use
1) Create a python3 virtual environment in your home folder, see:<br>
[https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)

```
python -m venv ~/my_python_venvs
```
2. Install the needed python packages

> the pymodbus documentation you will find here:<br>
[https://pymodbus.readthedocs.io/en/v3.9.2/](https://pymodbus.readthedocs.io/en/v3.9.2/)

```
~/my_python_venvs/bin/python -m pip install pymodbus==3.9.2
~/my_python_venvs/bin/python -m pip install pyserial
```
You can check the state by:

```
~/my_python_venvs/bin/python -m pip list
```



 ### Make your SMA Inverter ready to use
1. make sure that your SMA Device supports the modbus protocol
2. make sure that the SMA Device has started/enabled the TCP Server to communicate via modbus

## Library Installation
Install the library from github.<br>
Lets assume you want to install it in the following path: `~/git_repos`

```
cd ~
mkdir git_repos
cd git_repos
git clone https://github.com/hasenradball/SMA-SunnyBoy-Modbus.git
```
## Library Usage

Check the python code in the script `sma_modbus.py` and change the settings if necessary.<br>
Especially the `ip-address` has to be adapted to your settings in the following line:

```
sunny_obj = sunny_boy("192.168.xxx.xxx", UnitID)
```
The device UnitID has the value  `3` as default. If you are not sure you can use the funtion `read_device_unit_id()` to check.<br>
The UnitID can be set to values of `3...123`, the values `1` and `2` are reserved.<br>

Thus the constructor has a default parameter for the UnitID = 3, the instanciation can also be done like:
```
sunny_obj = sunny_boy("192.168.xxx.xxx")
```
### Check the UnitID
```
sunny_obj = sunny_boy("192.168.xxx.xxx")
print(sunny_obj.read_device_unit_id())
```

### Check the Communication
After updated the ip and the UnitID if necessary you can check the communication.


```
cd /path/to/your/installation/folder

~/my_python_venvs/bin/python sma_modbus.py
```

The result could look like this example:

```
SMA SunnyBoy Test

Device unit ID  : 3
Device class    : Solar-Wechselrichter
Serial Number   : xxxxxxxx
Software Packet : 50665988


INFO: test finished in 0.419 s

```
That's it!


# License
This library is licensed under MIT Licence.

# Helpful Links
* [ESP8266-01-Adapter](https://esp8266-01-adapter.de)
