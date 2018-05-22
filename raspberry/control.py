from __future__ import print_function

import bluetooth
import signal
import subprocess

import threading

import RPi.GPIO as GPIO
import time
import math
import sys


# GPIO setup #
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

GPIO.output(16, 0)
GPIO.output(18, 0)
pin_22 = GPIO.PWM(22, 50)
pin_24 = GPIO.PWM(24, 50)

pin_22.start(0)
pin_24.start(0)


# #### Bluetooth setup and data ##############################
# Server data
hostMAC = 'B8:27:EB:4F:E0:4B'
port = 0         # choose automatically 
backlog = 1
size = 1024

print("Bluetooth server started!")
print("Host MAC Address: {0}".format(hostMAC))

# Setting up bluetooth server
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMAC, port + 1))
s.listen(backlog)

print("Host port: {0}".format(str(s.getsockname()[1])))

# Making RPi discoverable with bluetooth
subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])


# #### Global variables #######################################
target_power = 0        # target power for power variable to lerp to
smooth_power = 0.01     # lerp smooth
power = 0               # actual power that will be applied in PWM
max_power = 7

turn_state = 1		# servo state  # 8.15
turn_vars = [5.5, 8.25, 11.5]	# servo directions
# LOWER - RIGHT    BIGGER - LEFT
bt_data = "z"		# data
last_bt_data = "z"	# last data

engine_data = ""
turn_data = ""
turn_flag = True


# #### Tools ##################################################
def lerp(a, b, t):
        return (a * (1 - t) + b * t)


def shift(arr, n):
        return arr[n:] + arr[:n]


# #### Bluetooth functions #####################################
# Closes server
def close_server():
	print("Server Closed!")
	s.close()

# Handles KeyInterrupt
# def signal_handler(signal, frame):
def quit():
        # when ctrl+c was pressed:
        # > close server
        # > exit from programm
        close_server()
        print("exiting programm!")
        sys.exit(0)



# #### Controling thread #########################################
def control_loop():
        print("Mind control initialized!")
        while True:
                global turn_vars, turn_state
                global target_power, smooth_power, power, max_power
		global bt_data, last_bt_data
		global turn_flag		

		# Calculating engine power
		# target_power = 0
		if bt_data == "w":
			target_power = max_power
			turn_state = 1
		if bt_data == "s":
			target_power = 0  # -max_power
			turn_state = 1
                                
                power = target_power

		# Calculating turn direction
                # if bt_data == 'a' or bt_data == 'd':
		#	if turn_flag == True:
		if bt_data == 'a':
                        turn_state = 2  # min(turn_state + 1, 2)
                if bt_data == 'd':
                        turn_state = 0  # max(turn_state - 1, 0)
		#		turn_flag = False

		# Calculating movement direction
                forward = 0
                backward = 0

                if power > 0:
                        forward = 0
                        # backward = 0
                elif power < 0:
                        forward = 1
                        # backward = 1

		# Applying calculated data to GPIO
                GPIO.output(16, forward)
                # GPIO.output(18, backward)
                pin_22.ChangeDutyCycle(abs(power))
                pin_24.ChangeDutyCycle(turn_vars[turn_state])
		
		# if bt_data != last_bt_data:	
		print('\r', power, forward, backward, turn_state, bt_data, end="              ")		
		# Saving last bluetooth data
                last_bt_data = bt_data


# #### Bluetooth Thread ######################################
# Listens for client
# Recieves data from client
def bt_listen_loop():
	while True:
		global bt_data, turn_flag
		try:
                	# Waiting for client to connect
			client, clientInfo = s.accept()
			print("Client Connected!")
			while 1:
                        	# checking for data being sent by client
				data = client.recv(size)
				if data:
					# print("Received: " + data)
					bt_data = data
					client.send(data)
					turn_flag = True
		except:
                	# When client disconnects, close connection with him
			print("Client disconnected!")
			client.close()


# #### Creating threads #######################################
# Checks for Ctrl+C for exit
# signal.signal(signal.SIGINT, signal_handler)
try:
        threading.Thread(target=bt_listen_loop).start()
        threading.Thread(target=control_loop).start()
except EnvironmentError as e:
        print(e)
        print("Error: could not create threads!")

