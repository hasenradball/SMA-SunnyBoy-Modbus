"""Script reading data from SMA SunnyBoy and send to mariaDB"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode
from cSMA_Modbus import SunnyBoy as sunny_boy
from mariadb_config import MARIA_DB_CONFIG
from cMariaDB_mysql import cMariaDB_mysql as maria_db

# Main
if __name__ == "__main__":
    sunny_obj = sunny_boy("192.168.178.29")
    power_total = sunny_obj.get_active_power()[0]
    i1_ac = sunny_obj.get_ac_current()[0]

    maria_obj = maria_db(MARIA_DB_CONFIG)
    maria_obj.insert_by_sql_insert_stmt("leistung", ("`p_act_sum`"), (power_total))
    maria_obj.insert_by_sql_insert_stmt("strom", ("`i_ac_l1`"), (i1_ac))
