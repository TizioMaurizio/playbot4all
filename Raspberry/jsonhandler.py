"""
USAGE:
loop() to do one step
send(json) to send a json, NOTE max size is 64 bytes due to arduinouino serial buffer limit

"""

import time
import serial
import json
import traceback

REC_RATE = 0.05
SEND_RATE = REC_RATE * 3

tosend = 0

arduino = serial.Serial('COM5', 2000000, timeout=REC_RATE) #CHANGE FOR RASPBERRY
arduino.flushInput()
arduino.flushOutput()

prevtime = 0

servo = True
asd = 0
yolo = 5
sendqueue = []
sending = 0
sent = 0
sendqueuestring = []

playbot = 0
    
def loop():
    global REC_RATE, SEND_RATE, tosend, arduino, prevtime, playbot
    
    currtime = time.time()
    if(currtime-prevtime > REC_RATE):
        tosend += REC_RATE
        
        received = arduino.readline()
        if(received):
            #print(asd)
            #print('\n')
            print(received)
            #print('\n')
            try:
                playbot = json.loads(received) #read the json
                ##print(playbot["servo"])
            except:
                pass
                #print("Json error")
        
        prevtime = currtime
        
        if(tosend >= SEND_RATE):
            tosend = 0
            #asd+=1
            #servo = not servo
            #if(asd == 20):
                #send({"servo":{"0":20,"1":20,"2":20,"3":20}})
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
        """
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
        """
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
   
def playbot():
    return playbot