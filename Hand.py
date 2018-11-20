import serial as s
import pandas
import os
import time

ser = s.Serial()
ser.baudrate = 9600
ser.port = "COM13"
ser.timeout = 1000
ser.open()
f = open('Hand.txt', 'wb')
f.write(b'XA,YA,ZA\r\n')
for i in range(0,10):

    x = ser.readline()
    print(x)
    f.write(x)

f.close()
ser.close()

data = pandas.read_csv("Hand.txt")

w