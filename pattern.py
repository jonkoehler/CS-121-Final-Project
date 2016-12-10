import os
import sys
import termios
import tty
import pigpio
import time
from thread import start_new_thread

#Pin numbers of each color (broadcom numbers)
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

#The value by which the color changes with each loop
STEPS     = 0.1


bright = 255        #highest value the lights can be set to
r = 255.0           #initial values of r, g, and b
g = 0.0
b = 0.0
color = "red"       #initial value of the string that makes sure the lights stay in the right order
pi = pigpio.pi()    #library 

#makes sure the values of the brightness stay between 0 and 255
def updateColor(color, step):
	color += step
	if color > 255:
		return 255
	if color < 0:
		return 0
	return color

#This function is taken from an open source script, NOT written by us
def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)

#starts the loop
while True:
                #fades red to off
		if r <= 255 and b == 0 and g == 0 and r != 0:              
			r = updateColor(r, -STEPS)
			setLights(RED_PIN, r)
			color = "red"

		#fades green from off to on 
		elif g == 0 and b == 0 and r == 0 and color == "red":
			while g < 255:
                                g = updateColor(g, STEPS)
                                setLights(GREEN_PIN, g)
                        color = "green"

		#fades green from on to off
		elif r == 0 and g == 255 and b == 0 and g > 0 and color == "green":
                        while g > 0:
                                g = updateColor(g, -STEPS)
                                setLights(GREEN_PIN, g)

		#fades blue from off to on
		elif r == 0 and b == 0 and g == 0 and color == "green":
                        while b < 255:
                                b = updateColor(b, STEPS)
                                setLights(BLUE_PIN, b)
                        color = "blue"

                #fades blue from on to off
		elif g == 0 and b == 255 and r == 0 and b > 0 and color == "blue":
                        while b > 0:
                                b = updateColor(b, -STEPS)
                                setLights(BLUE_PIN, b)

                #fade red from off to on        
		elif r == 0 and g == 0 and b == 0 and color == "blue":
                        while r < 255:
                                r = updateColor(r, STEPS)
                                setLights(RED_PIN, r)
                        color = "red"
