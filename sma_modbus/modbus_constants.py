"""module to prvide modbus constants"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ModbusConstants:
    """Constants for use with pymodbus
    """
    TYPE_TO_LENGTH = {'U8': 1, 'U16': 1, 'U32': 2, 'U64': 4, \
                      'S8': 1, 'S16': 1, 'S32': 2, 'S64': 4}

    DEVICE_CLASS   = {8000: 'Alle Geräte', \
                      8001: 'Solar-Wechselrichter', \
                      8002: 'Wind-Wechselrichter', \
                      8007: 'Batterie-Wechselrichter', \
                      8033: 'Verbraucher', \
                      8064: 'Sensorik Allgemein', \
                      8065: 'Stromzähler', \
                      8128: 'Kommunikationsprodukte'}

    DEVICE_TYPE    = {9074: 'SB 3000TL-21', \
                      9075: 'SB 4000TL-21', \
                      9076: 'SB 5000TL-21', \
                      9165: 'SB 3600TL-21', \
                      9098: 'STP 5000TL-20', \
                      9099: 'STP 6000TL-20', \
                      9100: 'STP 7000TL-20', \
                      9102: 'STP 9000TL-20', \
                      9103: 'STP 8000TL-20', \
                      9281: 'STP 10000TL-20', \
                      9282: 'STP 11000TL-20', \
                      9283: 'STP 12000TL-20'}

    DEVICE_STATUS  = { 35: 'Fehler', \
                      303: 'Aus', \
                      307: 'Ok', \
                      455: 'Warnung'}

    RELAY_STATE    = { 51: 'closed', \
                      311: 'open', \
                 16777213: 'information not available'}

    DERATING_CODE  = { 557: 'Temperature derating', \
                       884: 'not active', \
                  16777213: 'information not available'}
