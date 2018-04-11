import RPi.GPIO as GPIO
import string, subprocess, time, sys

led=12
led1=17
HIGH=1
LOW =0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
i=0
while i<2:
    GPIO.output(led, HIGH)
    print("LED on")
    GPIO.output(led1, HIGH)
    print("LED1 on")
    time.sleep(1)
    GPIO.output(led, LOW)
    print("LED off")
    GPIO.output(led1, LOW)
    print("LED1 off")
    time.sleep(1)
    i+=1
    
GPIO.cleanup()
exit(0)