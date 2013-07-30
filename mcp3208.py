#!/usr/bin/python
# -*- coding: utf-8 -*-
# mcp3208_lm35.py - read an 1k Themistisor on CH0 of an MCP3208 on a Raspberry Pi
# mostly nicked from
#  http://jeremyblythe.blogspot.ca/2012/09/raspberry-pi-hardware-spi-analog-inputs.html
# Also from
# http://scruss.com/blog/2013/02/02/simple-adc-with-the-raspberry-pi/
 
import spidev
import time
import math
import web
 
spi = spidev.SpiDev()
spi.open(0, 0)

#make a status global variable
#global tempc
#tempc = 0 

log = open('ttest1.txt', 'w') #open a text file for logging
print log #print what the log file is

#templates are in templates folder
render = web.template.render('templates/')

urls = ('/','index')
app = web.application(urls,globals())
 
def readadc(adcnum):
# read SPI data from MCP3208 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout


class index:
    def GET(self):
        getInput = web.input(turn="")
        command = str(getInput.turn)
        if command == "on":
            #temp_get()
            return render.index(temp_get())
    #raise web.seeother('/')
        if command == "off":
            #    set RPi board pins low
            #GPIO.output(28, GPIO.LOW)
            return "LED off"
        #else:
            #has to start by visiting /?turn=on 
         #   return render.index(tempc)

if __name__ == "__main__":
        app.run()

def temp_get():
    value = readadc(0) #read the adc
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
    #print out info
    print ("%4d/1023 => %5.3f V => %4.1f Ω => %4.1f °K => %4.1f °C" % (value, volts, ohms, temp, tempc))
    log.write('%f\n' % (tempc)) #write to log
    #time.sleep(10) #wait 10 seconds
    return tempc
 
# while True:
#     value = readadc(0) #read the adc
#     volts = (value * 3.3) / 1024 #calculate the voltage
#     ohms = ((1/volts)*3300)-1000 #calculate the ohms of the thermististor

#     lnohm = math.log1p(ohms) #take ln(ohms)

#     #a, b, & c values from http://www.thermistor.com/calculators.php
#     #using curve R (-6.2%/C @ 25C) Mil Ratio X
#     a =  0.002197222470870
#     b =  0.000161097632222
#     c =  0.000000125008328

#     #Steinhart Hart Equation
#     # T = 1/(a + b[ln(ohm)] + c[ln(ohm)]^3)

#     t1 = (b*lnohm) # b[ln(ohm)]

#     c2 = c*lnohm # c[ln(ohm)]

#     t2 = math.pow(c2,3) # c[ln(ohm)]^3

#     temp = 1/(a + t1 + t2) #calcualte temperature

#     tempc = temp - 273.15 - 4 #K to C
#     #print out info
#     print ("%4d/1023 => %5.3f V => %4.1f Ω => %4.1f °K => %4.1f °C" % (value, volts, ohms, temp, tempc))
#     log.write('%f\n' % (tempc)) #write to log
#     time.sleep(10) #wait 10 seconds



