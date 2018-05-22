import threading
import time
import os


def start(i):
	print("Running thread {0}".format(i))
	if i==0:
		time.sleep(1)
		print("Running: bt_server.py")
		os.system("sudo python2 /home/pi/Desktop/bt_server.py")
	if i==1:
		time.sleep(1)
		print("Running: mindcontrol.py")
		os.system("sudo python3 /home/pi/Desktop/mindcontrol.py")
	else:
		pass


for i in range(2):
        # t = threading.Thread(target=start, args=(i,))
        # t.start()
