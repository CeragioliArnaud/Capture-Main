import cv2, pandas
from datetime import datetime


"""

import serial as s
import pandas
import os
import time

ser = s.Serial()
ser.baudrate = 9600
ser.port = "COM6"
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

"""
first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])
i = 0
j=0
video = cv2.VideoCapture(0)

#Positions de bases

x1 = 170
y1 = 180
x2 = 210
y2 = 110
x3 = 260
y3 = 60
x4 = 300
y4 = 90
x5 = 340
y5 = 140
x6 = 250
y6 = 250

while True:

    check, frame = video.read()

    status = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (_, cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 12500:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    status_list.append(status)

    # Part where we extract datas

    data = pandas.read_csv("Hand.txt")
    xdata = list(data["XA"])
    ydata = list(data["YA"])
    zdata = list(data["ZA"])

    print(xdata, "+", ydata, "+", zdata)

    # Part which define fingers captors

    rgSqr = 25

    #le 19.9 s'obtient en passant de mètres en pixels *par rapport aux dimensions de la fênetre.

    if j==0:
        # Pouce
        x1p = x1+int(xdata[5*i]*19.9)
        y1p = y1+int(ydata[5*i]*19.9)
        # Index
        x2p = x2 + int(xdata[1 + 5 * i] * 19.9)
        y2p = y2 + int(ydata[1 + 5 * i] * 19.9)
        # Majeur
        x3p = x3 + int(xdata[2 + 5 * i] * 19.9)
        y3p = y3 + int(ydata[2 + 5 * i] * 19.9)
        # Annulaire
        x4p = x4 + int(xdata[3 + 5 * i] * 19.9)
        y4p = y4 + int(ydata[3 + 5 * i] * 19.9)
        # Auriculaire
        x5p = x5 + int(xdata[4 + 5 * i] * 19.9)
        y5p = y5 + int(ydata[4 + 5 * i] * 19.9)
        j+=1
    else:
        x1p += int(xdata[5 * i] * 19.9)
        y1p += int(ydata[5 * i] * 19.9)
        x2p += int(xdata[1 + 5 * i] * 19.9)
        y2p += int(ydata[1 + 5 * i] * 19.9)
        x3p += int(xdata[2 + 5 * i] * 19.9)
        y3p += int(ydata[2 + 5 * i] * 19.9)
        x4p += int(xdata[3 + 5 * i] * 19.9)
        y4p += int(ydata[3 + 5 * i] * 19.9)
        x5p += int(xdata[4 + 5 * i] * 19.9)
        y5p += int(ydata[4 + 5 * i] * 19.9)


    if i == 2:
        i=0
    else:
        pos1 = 0
        pouce = cv2.circle(frame, (x1p, y1p), 8, (0, 0, 255), -1)

        pos2 = 0
        index = cv2.circle(frame, (x2p, y2p), 8, (0, 0, 255), -1)

        pos3 = 0
        majeur = cv2.circle(frame, (x3p, y3p), 8, (0, 0, 255), -1)

        pos4 = 0
        annulaire = cv2.circle(frame, (x4p, y4p), 8, (0, 0, 255), -1)

        pos5 = 0
        auriculaire = cv2.circle(frame, (x5p, y5p), 8, (0, 0, 255), -1)

    # Capteur Mother

    pos6 = 0
    captBoss = cv2.rectangle(frame, (x6 - rgSqr, y6 - rgSqr), (x6 + rgSqr, y6 + rgSqr), (0, 255, 0), 3)

    pce2BOM = cv2.line(frame, (x1p, y1p), (x6, y6), (255, 0, 0), 3)
    ind2BOM = cv2.line(frame, (x2p, y2p), (x6, y6), (255, 0, 0), 3)
    maj2BOM = cv2.line(frame, (x3p, y3p), (x6, y6), (255, 0, 0), 3)
    ann2BMOM = cv2.line(frame, (x4p, y4p), (x6, y6), (255, 0, 0), 3)
    aur2BMOM = cv2.line(frame, (x5p, y5p), (x6, y6), (255, 0, 0), 3)

    i += 1

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'Hand_project: LPSIL IDSE', (10, 30), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("Gray frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)

df.to_csv("Capture.csv")

video.release()
cv2.destroyAllWindows()
