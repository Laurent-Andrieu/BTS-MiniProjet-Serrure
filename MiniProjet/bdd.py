#!/usr/bin/python3

# /*--------------------------------------------------------------------*/
# /*    Auteur: Laurent Andrieu                                         */
# /*    Date: 10/01/2020                                                */
# /*    Desc: mini projet                                               */
# /*--------------------------------------------------------------------*/

import mysql.connector
import time
import subprocess
from MiniProjet import uart

pwd = ""
loc_pwd = ""


def rx_info():
    data = rx_data.decode("utf-8").split(",")
    usr_code = data[1]
    sens = data[2]
    return usr_code, sens


def bdd_fetch(table):
    cursor.execute(f"SELECT * FROM {table}")
    output = cursor.fetchall()
    return output


def db_write(table, val, col):
    cursor.execute(f"INSERT INTO {table} ({col[0]},{col[1]},{col[2]}) VALUES ('{val[0]}', ' {val[1]}', '{val[2]}')")
    mydb.commit()


def user_check():
    usr = bdd_fetch("utilisateurs")
    code = rx_info()[0]
    for info in usr:
        if code in info[3]:
            return True, info[0], info[2], info[3]


mydb = None
while not mydb:
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="laurent",
            passwd=pwd,
            database="serrure"
        )
        if mydb:
            print(f"\nConnected to '{mydb.database}'")
    except Exception as conerr:
        print("Tentative de reconnection")
        subprocess.call(f"echo {loc_pwd} | sudo -S systemctl start mysql", shell=True)

cursor = mydb.cursor()

rx = uart.init_serial("/dev/ttyUSB0")
tx = uart.init_serial("/dev/ttyUSB1")

while True:
    rx_data = uart.get_data(rx)
    user_check()
    date_a = time.strftime('%Y-%m-%d %H:%M:%S')

    if user_check()[0] is True:
        db_write("journal", (user_check()[1], date_a, rx_info()[1]), ("user_id", "date_action", "sens"))
        uart.write_data(tx, bytes("1", "utf-8"))
        print(f"User {user_check()[2]}:{user_check()[3]} is allowed")
    else:
        print(f"User is not allowed")
