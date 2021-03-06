"""
USAGE:
loop() to do one step
send(json) to send a json, NOTE max size is 64 bytes due to arduinouino serial buffer limit

IMPORTANT:
"""

import time
import serial
import json
import traceback
from pbdebug import debug as debug
#import keyboard

PRINT_RECEIVED = True
REC_RATE = 0.05
SEND_RATE = REC_RATE * 4
path = "/home/pi/Desktop/playbot4all/Raspberry/"
tosend = 0
debug("jsonhandler begin")

for i in range(1000):
    try:
        usbport = str('/dev/ttyACM0')#str('COM7')#
        arduino = serial.Serial(usbport, 2000000, timeout=REC_RATE)#CHANGE FOR RASPBERRY
        debug("usb connected")
        break
    except:
        pass
#arduino.flushInput()
#arduino.flushOutput()
prevtime = 0

servo = True
asd = 0
yolo = 5
sendqueue = []
sending = 0
sent = 0
sendqueuestring = []
ERROR = 0
playbot = 0
CONNECTION_RESET = False

def loop():
    #debug("jsonhandler loop")
    global REC_RATE, SEND_RATE, tosend, arduino, prevtime, playbot, ERROR, CONNECTION_RESET, PRINT_RECEIVED
    currtime = time.time()
    if(currtime-prevtime > REC_RATE):
        tosend += REC_RATE
        try:
            received = arduino.readline()
        except:
            CONNECTION_RESET = True
            print('RESETTING SERIAL')
            arduino.close()
            try:
                arduino = serial.Serial(usbport, 2000000, timeout=REC_RATE) #CHANGE FOR RASPBERRY
            except:
                pass
            #arduino.flushInput()
            #arduino.flushOutput()
            
        if(received):
            ERROR = 0
            #print(asd)
            #print('\n')
            
            #print('\n')
            try:
                playbot = json.loads(received) #read the json
                ##print(playbot["servo"])
            except:
                pass
                #print("Json error")
            if(PRINT_RECEIVED):
                print(received)
        else:
            ERROR = ERROR + 1
            if(ERROR > 100):
                CONNECTION_RESET = True
                print('RESETTING SERIAL')
                arduino.close()
                try:
                    arduino = serial.Serial(usbport, 2000000, timeout=REC_RATE) #CHANGE FOR RASPBERRY
                except:
                    pass
                #arduino.flushInput()
                #arduino.flushOutput()
                ERROR = 0
        prevtime = currtime
        
        if(tosend >= SEND_RATE):
            tosend = 0
            #asd+=1
            #servo = not servo
            #if(asd == 20):
                #send({"servo":{"0":360,"1":360,"2":360,"3":360}})
            #if(asd == 30):
                #send({"led":{"0":20,"1":20,"2":20,"3":20}})
            ack()
            
            #if(servo):
                #arduino.write(json.dumps({"servo":{"0":asd,"1":asd,"2":asd,"3":asd}}).encode())
            #if(servo):
                #arduino.write(json.dumps({"servo":{"0":5,"1":5,"2":5,"3":5}}).encode())
            
            #arduino.write(json.dumps(sending).encode())
                
            #else:
                #arduino.write(json.dumps({"led":{"0":asd,"1":asd,"2":asd,"3":asd}}).encode())
  
staging = dict() 
stamp = 0
sending = 0
prevSend = 0
isSending = False
sendQueue = list()

def send(toSend):
    global sending, prevSend, isSending, sendQueue
    prevSend = sending
    sending = toSend
    if prevSend != sending:
        if len(sendQueue) == 4:
            sendQueue.pop(0)
        if sending not in sendQueue:
            sendQueue.append(sending)
        else:
            for i in sendQueue:
                if i == sending:
                    sendQueue.remove(i)
            sendQueue.append(sending)
        #print("QUEUE", sendQueue)
        isSending = True
    return 1

def ack():
    global sending, isSending  
    try:
        sendElement = sendQueue.pop(0)
        arduino.write(json.dumps(sendElement).encode())
        #print("SEND", sendElement)
    except:
        pass
    """if isSending: #Send only when message is different
        print(sending)
        arduino.write(json.dumps(sending).encode())
        isSending = False
    """
    #print(json.dumps(sending).encode())
"""
def send(toSend):
    global sending, sent, sendqueuestring, sendqueue, staging
    
    for field in toSend:
        staging[field] = toSend[field]
        
    #print(staging)
    try:    
        #print('\n')
        #print(staging)
        sendqueue = []
        sendqueuestring = []
        for field in staging:
            sendqueue.append({field:staging[field]})
            sendqueuestring.append(json.dumps({field:staging[field]}).encode())
        #print(sendqueue)
        
        return 1
        ##
        #print(toSend["servo"])
        for i in sendqueue:
                
                try:
                    #print("asd")
                    if sendqueue[i]["servo"]:
                        print("asd")
                        print(field)
                        sendqueue.pop(i)
                except:
                    pass
        sendqueue.append(toSend)
        for i in sendqueue:
            print(len(sendqueue))
            print(sendqueue[len(sendqueue)-1]["servo"])
            
        sendqueuestring.append(json.dumps(sendqueue[len(sendqueue)-1]).encode())
        if len(sendqueue)>2:
            sendqueue = sendqueue[:2]
            sendqueuestring = sendqueuestring[:2]
            return 0
        print(len(sendqueue))
        ##
    except:
        pass
        #print("push error")
        #traceback.print_exc()
    
def ack():
    global arduino, sendqueue, sendqueuestring, playbot, staging
    #print(sendqueue)
    if(len(sendqueue) == 0):
        staging = dict()
        return
    try:
        #if len(sendqueuestring)==0:
            #print("empty buffer")
        arduino.write(sendqueuestring[0])
        print(sendqueuestring[0])
        for field in sendqueue[0]:
            ##print(sendqueue)
            #print('\n')
            #print(sendqueuestring)
            if playbot[field] != sendqueue[0][field]:
                return
        sendqueue.pop(0)
        sendqueuestring.pop(0)
        #print('popped')
    except Exception as e:
        pass
        #print("send error")
        #traceback.#print_exc()
"""
def getPlaybot():
    return playbot

debug("jsonhandler end")