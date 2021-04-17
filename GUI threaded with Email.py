import smtplib
import serial
from guizero import *
from time import sleep
from math import pi
from threading import*

#serial setup
ArduinoSerial = serial.Serial('COM4', 9600)
ArduinoSerial.flush()
sleep(3)


def Email():
    while True:
        ArduinoSerial.flush()
        ardData = ArduinoSerial.readline().decode('utf-8')
        if ardData == "Finished\n":
            content = "Patient 0's injection is complete"

            toAddress = 'W0283554@campus.nscc.ca'   # where you want the message sent to

            fromAddress = 'AutoSyringePumpProject@gmail.com'  # this really doesn’t matter

            subject = 'Injection Complete'

            header = 'To:' + toAddress + '\n' + 'From:' + fromAddress + '\n' + 'Subject:' + subject

            mail = smtplib.SMTP('smtp.gmail.com', 587)

            mail.ehlo()

            mail.starttls()

            mail.login('YourEmail@Email.com', 'THIS IS THE PASSWORD')  # your gmail account info

            mail.sendmail( fromAddress, toAddress, header + '\n\n' + content)

            mail.close()


def Forward_Step():
    ArduinoSerial.write(str('F').encode('utf-8'))
    ArduinoSerial.write(str('\n').encode('utf-8'))
    ArduinoSerial.flush()

    vol = float(setDose.value)
    vol = vol / 1000000
    t = float(setTime.value)
    r = 0.009565  # m
    l = 0.002  # m

    h = vol / (pi * (r ** 2))
    s = h / t

    rpm = s / (l * 4)
    rot = h / (l * 4.5)  # distance/(pitch*number of starts on screw)

    ArduinoSerial.write(str(rpm).encode('utf-8'))
    ArduinoSerial.write(str(',').encode('utf-8'))
    ArduinoSerial.flush()
    ArduinoSerial.write(str(rot).encode('utf-8'))
    ArduinoSerial.write(str('\n').encode('utf-8'))
    sleep(.05)
    ArduinoSerial.flush()


def Reverse_Step():
    ArduinoSerial.write(str('B').encode('utf-8'))
    ArduinoSerial.write(str('\n').encode('utf-8'))
    ArduinoSerial.flush()


def ExitGUI():
    app.destroy()


app = App("Rituximab Syringe Pump Interface", height = 900, width=1000)

forwardbox = Box(app)
fwdtxt = Text(forwardbox, text="Enter Constraints: ")
Forward = PushButton(forwardbox, text = "Forward Step", command = Forward_Step, width = 100, height=10)
Timeheader = Text(forwardbox, text="Time in minutes")
setTime = Slider(forwardbox, start=0, end=7, width="fill", height=50)
DoseHeader = Text(forwardbox, text="Dose in mL")
setDose = Slider(forwardbox, start=0, end=20, width="fill", height=50)

Reverse = PushButton(app, text = "Reverse Step", command = Reverse_Step, width = 100, height=10)
ExitG = PushButton(app, text = "Exit", command = ExitGUI, width = 100, height=10)
#possible going to remove pause botton entirely as any botton pressed during the main arduino loop will stop motor

t1 = Thread(target = Email)
t1.start()
app.display()
ArduinoSerial.close()