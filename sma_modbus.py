#!/usr/bin/python3
# -*- coding: utf-8 -*-

from cSMA_Modbus import Sunnyboy5000TL21 as sunny_boy

# Main
if __name__ == "__main__":
    sunny_obj = sunny_boy("192.168.178.29")
    sunny_obj.connect()
    print(f'Device class    : {sunny_obj.get_device_class()}')
    print(f'Serial Number   : {sunny_obj.get_serial_number()}')
    print(f'Software Packet : {sunny_obj.get_software_packet()}')
    print(f'Device Type     : {sunny_obj.get_device_type()}')
    print("\n")
    print(f'Status of Device : {sunny_obj.get_status_of_device()}')
    print(f'Derating         : {sunny_obj.get_derating()}')
    print(f'Grid Relay state : {sunny_obj.get_grid_relay_status()}')
    print ("\n")
    print(f'Total yield  : {sunny_obj.get_total_yield()} Wh')
    print(f'Daily yield  : {sunny_obj.get_daily_yield()} Wh')
    print(f'Operating time  : {sunny_obj.get_operating_time()} s')
    print(f'feed-in time    : {sunny_obj.get_feed_in_time()} s')
    print ("\n")
    print(f'DC Current In : {sunny_obj.get_dc_current_in()} A')
    print(f'DC Voltage In : {sunny_obj.get_dc_voltage_in()} V')
    print(f'DC Power In   : {sunny_obj.get_dc_power_in()} W')
    print ("\n")
    print(f'Active Power : {sunny_obj.get_active_power()} kW')
    print(f'AC Current   : {sunny_obj.get_ac_current()} A')
    sunny_obj.close()
    print ("\n")
    print("INFO: test finished!")
    
