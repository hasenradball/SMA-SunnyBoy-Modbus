'''Modbus Constants'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ModbusConstants:
    '''Constants for use with pymodbus
    '''
    TYPE_TO_LENGTH = {'U8': 1, 'U16': 1, 'U32': 2, 'U64': 4, \
                      'S8': 1, 'S16': 1, 'S32': 2, 'S64': 4}
