import time
import serial
RATE = 0.05
ard = serial.Serial('COM5', 115200, timeout=0.05)
currtime = time.time()
prevtime = 0
sendtime = currtime
while True:
    currtime = time.time()
    if(currtime-prevtime > RATE):
        x = ard.readline()
        if(x):
            print(x)
            print('\n')
            print(currtime-prevtime)
        prevtime = currtime
        
    if(currtime-sendtime > 3):
        print('send\n')
        ard.write(b'{"servo":1}\n')
        #ard.write(b'{"servo":{"hip_right":0,"leg_right":0,"hip_left":0,"leg_left":0}, "led":{"top":0,"right":0,"left":0,"back":0}}')
        sendtime = currtime
    