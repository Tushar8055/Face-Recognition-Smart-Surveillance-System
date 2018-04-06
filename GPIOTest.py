import RPi.GPIO as GPIO
import string, subprocess, time, sys

led = 17
HIGH=1
LOW =0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT) 
i=0
while i<2:
    GPIO.output(led, HIGH)
    print("LED on")
    time.sleep(1)
    GPIO.output(led, LOW)
    print("LED off")
    time.sleep(1)
    i+=1
    
GPIO.cleanup()