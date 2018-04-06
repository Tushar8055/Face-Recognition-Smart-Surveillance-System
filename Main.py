import RPi.GPIO as GPIO
import smtplib, string, subprocess, time, sys, os
import MySQLdb

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from subprocess import call

db = MySQLdb.connect(host = "localhost", user = "root", passwd = "raspberry", db = "mydb")
curs=db.cursor()

print("System Working")
SMTP_USERNAME = 'raspicamera03@gmail.com'
SMTP_PASSWORD = 'R@spberryPi3'
SMTP_RECIPIENT = 'tushargenius2013@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SSL_PORT = 465

led=17
pir=18
HIGH=1
LOW=0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(pir,GPIO.IN)

def write_db(name):
    DATE = time.strftime('%Y-%m-%d')
    TIME = time.strftime('%H:%M:%S')
    print("Writing into Database")
    try:
        curs.execute("""INSERT INTO Visitors (Date, Time, Name) values(%s, %s, %s)""",(DATE,TIME,name))
        db.commit()

    except:
        db.rollback()

def sendMail():
    toaddr = SMTP_RECIPIENT
    fromaddr = SMTP_USERNAME
    mail = MIMEMultipart()
    mail.preamble = 'Rpi Sends image'
    mail['Subject'] = "Movement Detected"
    body = " has entered the premises"

    os.system("python CheckFace.py -dir '/home/pi/scripts/camera/Intruder.jpg'")
    name = ""
    for item in os.listdir('/home/pi/scripts/camera/'):
        name  = item
        break
    
    append = ""
    
    for i in range(len(name)):
        if name[i]=='.':
            break
        append += name[i]  
    
    if append == "Intruder":
        body = "Intruder"+body
    else:
        body = append+body
    
    attachment = open('/home/pi/scripts/camera/'+name, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(MIMEText(body, 'plain'))
    print("Uploading Attachment")
    mail.attach(image)
    print("Sending the mail")
    server = smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT)
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(fromaddr, toaddr, mail.as_string())
    server.quit()
    os.unlink('/home/pi/scripts/camera/'+name)
    print("Mail sent")
    write_db(append)
    print("----------------------------------")

def capture_image():
    call(["raspistill -n -t 1000 -awb auto -ISO auto --exposure auto -o /home/pi/scripts/camera/Intruder.jpg -w 1920 -h 1080"], shell=True)
    print("Image Shot")
    p = subprocess.Popen(["runlevel"], stdout=subprocess.PIPE)
    out, err=p.communicate()
    if out[2] == '0':
        print('Halt detected')
        exit(0)
    if out [2] == '6':
        print('Shutdown detected')
        exit(0)
    print("Connected to mail")
    sendMail()

while True:
    if GPIO.input(pir)==1:
        print("Movement Detected")
        GPIO.output(led, HIGH)
        GPIO.output(led, LOW)
        GPIO.output(led, HIGH)
        capture_image()
        while(GPIO.input(pir)==1):
            time.sleep(1)
        
    else:
        GPIO.output(led, LOW)
        time.sleep(0.01)

GPIO.cleanup()
exit(0)