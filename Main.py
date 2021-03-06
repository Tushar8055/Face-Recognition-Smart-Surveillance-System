import RPi.GPIO as GPIO
import smtplib, string, subprocess, time, sys, os
import MySQLdb
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from subprocess import call

db = MySQLdb.connect(host = "localhost", user = "root", passwd = "Password", db = "mysql")
curs=db.cursor()

print("System Working")
SMTP_USERNAME = 'fromaddress@gmail.com'
SMTP_PASSWORD = 'Password'
SMTP_RECIPIENT = 'toaddress@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SSL_PORT = 465

led1=17
led=12
pir=18
HIGH=1
LOW=0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(led1,GPIO.OUT)
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

def verify(name):
    namelist = ['John', 'Victor', 'James', 'Sara', 'Barry', 'Richard']
    if name in namelist:
        GPIO.output(led,HIGH)
        time.sleep(3)
        GPIO.output(led,LOW)
    else:
        GPIO.output(led,LOW)

def sendMail(append,name):
    print("Connected to mail")
    print("Composing Mail")
    toaddr = SMTP_RECIPIENT
    fromaddr = SMTP_USERNAME
    mail = MIMEMultipart()
    mail.preamble = 'Rpi Sends image'
    mail['Subject'] = "Movement Detected"
    body = " has entered the premises"

    if append == "Intruder":
        body = "Intruder"+body
    else:
        body = append+body

    attachment = open('/home/pi/script/camera/'+name, 'rb')
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
    os.unlink('/home/pi/script/camera/'+name)
    print("Mail sent")
    write_db(append)
    print("----------------------------------")

def RecogniseFace():
    print("Recognising Face")
    os.system("python CheckFace.pyc -dir '/home/pi/script/camera/Intruder.jpg'")
    name = ""
    for item in os.listdir('/home/pi/script/camera/'):
        name  = item
        break

    append = ""

    for i in range(len(name)):
        if name[i]=='.':
            break
        append += name[i]
        
    if append != "Intruder":
        print("Face Recognised")
    
    verify(append)
    sendMail(append,name)

def capture_image():
    call(["raspistill -n -t 1000 -awb auto -ISO auto --exposure auto -o /home/pi/script/camera/Intruder.jpg -w 1280 -h 720"], shell=True)
    print("Image Shot")
    p = subprocess.Popen(["runlevel"], stdout=subprocess.PIPE)
    out, err=p.communicate()
    if out[2] == '0':
        print('Halt detected')
        exit(0)
    if out [2] == '6':
        print('Shutdown detected')
        exit(0)
    RecogniseFace()

while True:
    if GPIO.input(pir)==1:
        print("Movement Detected")
        GPIO.output(led1, HIGH)
        capture_image()
        GPIO.output(led1, LOW)
        GPIO.output(led1, HIGH)
        while(GPIO.input(pir)==1):
            time.sleep(1)

    else:
        GPIO.output(led1, LOW)
        time.sleep(0.01)

GPIO.cleanup()
exit(0)
