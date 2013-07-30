#!/usr/bin/python
# -*- coding: utf-8 -*-
# mcp3008_lm35.py - read an LM35 on CH0 of an MCP3008 on a Raspberry Pi
# mostly nicked from
#  http://jeremyblythe.blogspot.ca/2012/09/raspberry-pi-hardware-spi-analog-inputs.html
 
import spidev
import time
import math
 
spi = spidev.SpiDev()
spi.open(0, 0)

f = open('ttest1.txt', 'w')
print f
 
def readadc(adcnum):
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout
 
while True:
    value = readadc(0)
    volts = (value * 3.3) / 1024
    ohms = ((1/volts)*3300)-1000
    lnohm = math.log1p(ohms)
    a =  0.002197222470870
    b =  0.000161097632222
    t1 = (b*lnohm) 
    c =  0.000000125008328
    c2 = c*lnohm
    #c2 = math.pow(8.587749408080068,-7)
    t2 = math.pow(c2,3)
    temp = 1/(a + t1 + t2)
    tempc = temp - 273.15 - 4
    print ("%4d/1023 => %5.3f V => %4.1f Ω => %4.1f °K => %4.1f °C" % (value, volts,
            ohms, temp, tempc))
    f.write('%f\n' % (tempc))
    #print ("%f" % c2)
    time.sleep(10)
