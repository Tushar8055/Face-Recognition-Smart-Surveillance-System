import RPi.GPIO as GPIO
import string, subprocess, time, sys

led=17
pir=18
HIGH=1
LOW =0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(led, GPIO.OUT)         #LED output pin

while True:
    if GPIO.input(pir)==0:                 #When output from motion sensor is LOW
        print "No intruders"
        GPIO.output(led, LOW)  #Turn OFF LED
        time.sleep(0.1)
    elif GPIO.input(pir)==1:               #When output from motion sensor is HIGH
        print "Intruder detected"
        GPIO.output(led, HIGH)  #Turn ON LED
        time.sleep(0.1)
        
GPIO.cleanup()