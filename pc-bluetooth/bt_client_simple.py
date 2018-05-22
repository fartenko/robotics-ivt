import bluetooth
import getch
import itertools
import operator

serverMAC = 'B8:27:EB:4F:E0:4B'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMAC, port))




while True:
    # stream data here
    char = getch.getch()
    if char == "q":
        break

    s.send(char)


s.close()
