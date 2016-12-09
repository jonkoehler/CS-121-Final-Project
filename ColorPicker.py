# Pin numbers
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

import os
import sys
import termios
import tty
import pigpio
import time
from thread import start_new_thread

#global variables 
bright = 255
r = 255.0
g = 0.0
b = 0.0
rBright = 0
gBright = 0
bBright = 0


abort = False         #set the killl switch to false

pi = pigpio.pi()      #the program it's interacting with 

#function sets the color of the lights with a value from 0 to 255
def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)

#fuction gets the key presses
def getCh():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch


def checkBright():
    global rBright 
    global bBright 
    global gBright

    if rBright > 255:
        rBright = 255
        print ("Red doesn't go any brighter!")

    if rBright < 0:
        rBright = 0
        print ("Red doesn't go any dimmer!")    

    if gBright > 255:
        gBright = 255
        print ("Green doesn't go any brighter!")

    if gBright < 0:
        gBright = 0
        print ("Green doesn't go any dimmer!")    

    if bBright > 255:
        bBright = 255
        print ("Blue doesn't go any brighter!")

    if bBright < 0:
        bBright = 0
        print ("Blue doesn't go any dimmer!")    


def checkKey():
	global abort
        global rBright 
        global bBright 
        global gBright
	
	while True:
		c = getCh()

		if c == 'r':
			time.sleep(0.01)
			rBright += 10
			checkBright()
			setLights(RED_PIN, rBright)
			print ("Red Brightness: "+ str(rBright))

                if c == '1':
			time.sleep(0.01)
			rBright -= 10
			checkBright()
			setLights(RED_PIN, rBright)
			print ("Red Brightness: "+ str(rBright))

			
		if c == 'g':
			time.sleep(0.01)
			gBright += 10
			checkBright()
			setLights(GREEN_PIN, gBright)
			print ("Green Brightness: "+ str(gBright))

		if c == '2':
			time.sleep(0.01)
			gBright -= 10
			checkBright()
			setLights(GREEN_PIN, gBright)
			print ("Green Brightness: "+ str(gBright))

                if c == 'b':
			time.sleep(0.01)
			bBright += 10
			checkBright()
			setLights(BLUE_PIN, bBright)
			print ("Blue Brightness: "+ str(bBright))

		if c == '3':
			time.sleep(0.01)
			bBright -= 10
			checkBright()
			setLights(BLUE_PIN, rBright)
			print ("Blue Brightness: "+ str(bBright))
			
		if c == 'c' and not abort:
			abort = True
			break

start_new_thread(checkKey, ())


print ("+ / - = Increase / Decrease brightness")
print ("p / o = Pause / Resume")
print ("c = Abort Program")
print ("r = Increase Red")
print ("b = Increase Blue")
print ("g = Increase Green")
print ("1 = Decrease Red")
print ("2 = Decrease Green")
print ("3 = Decrease Blue")
    
while abort == False:
    if abort == True:
        print ("Aborting...")

        setLights(RED_PIN, 0)
        setLights(GREEN_PIN, 0)
        setLights(BLUE_PIN, 0)

        time.sleep(0.5)

        pi.stop()
