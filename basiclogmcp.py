#!/usr/bin/python
# -*- coding: utf-8 -*-
# A simple script to log data from the MCP3208
# Based off mcp3208.py

import spidev
import time
import math
from time import strftime

spi = spidev.SpiDev()
spi.open(0, 0)

log = open('logtest1.txt', 'w') #open a text file for logging
print log #print what the log file is
log.write('Time,Inside,Outside\n') #write to log

 
def readadc(adcnum):
# read SPI data from MCP3208 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

#thermistor reading function
def temp_get(adc):
    value = readadc(adc) #read the adc
    volts = (value * 3.3) / 1024 #calculate the voltage
    ohms = ((1/volts)*3300)-1000 #calculate the ohms of the thermististor

    lnohm = math.log1p(ohms) #take ln(ohms)

    #a, b, & c values from http://www.thermistor.com/calculators.php
    #using curve R (-6.2%/C @ 25C) Mil Ratio X
    a =  0.002197222470870
    b =  0.000161097632222
    c =  0.000000125008328

    #Steinhart Hart Equation
    # T = 1/(a + b[ln(ohm)] + c[ln(ohm)]^3)

    t1 = (b*lnohm) # b[ln(ohm)]

    c2 = c*lnohm # c[ln(ohm)]

    t2 = math.pow(c2,3) # c[ln(ohm)]^3

    temp = 1/(a + t1 + t2) #calcualte temperature

    tempc = temp - 273.15 - 4 #K to C
    # the -4 is error correction for bad python math

    #print out info
    print ("%4d/1023 => %5.3f V => %4.1f Ω => %4.1f °K => %4.1f °C from adc %d" % (value, volts, ohms, temp, tempc, adc))
    #log.write('%f, %d\n' % (tempc, adc)) #write to log
    #time.sleep(10) #wait 10 seconds
    return tempc

while True:
	log.write('%s,%f,%f\n' % (strftime("%H:%M"), temp_get(0), temp_get(1))) #write to log
	#temp_get(0)
	#temp_get(1)
	time.sleep(60)
    #return render.index(round(temp_get(adc),1))