#!/usr/bin/python3

# /*--------------------------------------------------------------------*/
# /*    Auteur: Laurent Andrieu                                         */
# /*    Date: 10/01/2020                                                */
# /*    Desc: mini projet                                               */
# /*--------------------------------------------------------------------*/

import serial


def init_serial(port):
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = 9600
    ser.bytesize = 8
    ser.parity = "N"
    ser.stopbits = 1
    ser.timeout = 5
    ser.xonxoff = False
    ser. rtscts = False
    ser.dsrdtr = False
    if not ser.is_open:
        try:
            ser.open()
        except Exception as exc:
            print(exc)
    return ser


def get_data(ser):
    if ser.is_open:
        while ser.is_open:
            return ser.readline()
    else:
        print("Serial port is not opened")


def write_data(ser,data):
    if ser.is_open:
        ser.write(bytes(f"{data}", "utf-8"))
        ser.close()
