import os
count = 0
while count < 30:
    count += 1
    os.system('raspistill -n -t 1000 -ISO auto -awb auto --exposure auto -o /home/pi/Pictures/'+str(count)+'.jpg')
    print(str(count))