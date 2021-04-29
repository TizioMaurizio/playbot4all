import time
import serial
import json

RATE = 0.1
ard = serial.Serial('COM5', 2000000, timeout=RATE)
ard.flushInput()
ard.flushOutput()
currtime = time.time()
prevtime = 0
sendtime = currtime

asd = 0
while True:
    currtime = time.time()
    if(currtime-prevtime > RATE):
        asd+=1
        x = ard.readline()
        if(x):
            print(asd)
            print('\n')
            print(x)
            print('\n')
            print(currtime-prevtime)
            if(asd%2):
                ard.write(json.dumps({"servo":{"0":asd,"1":asd,"2":asd,"3":asd}}).encode())
            else:
                pass#ard.write(json.dumps({"led":{"0":asd,"1":asd,"2":asd,"3":asd}}).encode())
        
        prevtime = currtime
        
    t = 0.1    
    if(currtime-sendtime > 999999999):
        print('send\n')
        #ard.write(b'{"servo":1}\n0')
        #ard.write(b'{"servo":{"hip_right":0}}\n')
        #ard.write(b'{"capacitive":false,"analog":{"x":0,"y":0},"rotary":0,"irsensor":false}')
        #ard.write(b'{"servo":{"hip_right":0,"leg_right":0,"hip_left":0,"leg_left":0}, "led":{"top":0,"right":0,"left":0,"back":0}}\n0')
        #ard.write(b'{"servo":{"hip_right":0,"leg_right":0,"hip_left":0,"leg_left":0')
        #time.sleep(0.05)
        #ard.write(b'}, "led":{"top":0,"right":0,"left":0,"back":0}}\n')
        #ard.write(b'{"servo":{"hip_right":0,"leg_right":0,"hip_left":0,"leg_left":0')
        #while(not ard.read()):
            #pass
        #ard.write(b'}, "led":{"top":0,"right":0,"left":0,"back":0}}\n<')
        #ard.write(b'{"servo":[0,0,0,0]\n')
        #time.sleep(0.1)
        #ard.write(b'{"led":{"1":0,"2":0,"3":0,"4":0}}\n')
        #ard.write(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n')
        #ard.write(b'{"servo":{"a":0,"b":0,"c":0,"d":0}, "led":{"1":0,"2":0,"3":0,"4":0}}\n')
        ard.write(json.dumps({"servo":{"0":0,"1":0,"2":0,"3":0}}).encode())
        ard.write(json.dumps({"led":{"0":"YE","1":"YE","2":"YE","3":"YE"}}).encode())
        #, "led":{"top":0,"right":0,"left":0,"back":0}}).encode())
        #ard.write(json.dumps({"servo":{"hip_right":0,"leg_right":0,"hip_left":0,"leg_left":0}})), "led":{"top":0,"right":0,"left":0,"back":0}}).encode())
        sendtime = currtime