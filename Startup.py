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

GPIO.output(led, HIGH)
print("LED on")
GPIO.output(led1, HIGH)
print("LED1 on")
time.sleep(5)
GPIO.output(led, LOW)
print("LED off")
GPIO.output(led1, LOW)
print("LED1 off")

GPIO.cleanup()
exit(0)