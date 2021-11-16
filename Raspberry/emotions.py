import jsonhandler
import time
import serial
import json
import traceback

#example to increase an emotion: import emotions, emotions.increase("joy", 200): this will make the robot happy for at least 200 seconds
#every EMOTION_TICK seconds every emotion score is reduced by DELAY down to zero

colors = {"anger": [255,0,0],"fear": [0,255,0],"blue": [0,0,255],"joy": [255,128,0],"cyan": [0,255,255],"purple": [255,0,255],"white": [255,255,255]}
emotions = {"joy": 60, "anger": 120, "fear": 0}

DECAY = 1 #second
EMOTION_TICK = 1 #second
prevtime = 0
EMOTION_MAX = 240 #maximum score for emotions

#TODO
#blink when emotion score is very high
#smooth transition between colors
def emotion(emot):
    #todo emotion function, mind that import increases joy by 2000 as of now
    pass
    
def loop():
    global prevtime
    currtime = time.time()
    if (currtime - prevtime > EMOTION_TICK):
        prevtime = currtime
        current_emotion = max(emotions, key=emotions.get) #choose the emotion with the maximum score
        if emotions[current_emotion] == 0:
            jsonhandler.send({"rgb": colors["fear"]}) #neutral is fear?
        else:
            send_color = colors[current_emotion]
            jsonhandler.send({"rgb": send_color})
                
        #increase fear when not interacting?
        #emotions["fear"] += 2
        
        #increase joy with petting
        try:
            if jsonhandler.getPlaybot()["capacitive"]:
                emotions["joy"] += 3
        except:
            print("no capacitive")
            
        #increase anger if lying down
        try:
            if jsonhandler.getPlaybot()["pose"] == 'face_up':
                emotions["anger"] += 1
        except:
            print("no pose")
            
        for emot in emotions:
            if emotions[emot]>0:
                emotions[emot] -= DECAY
            if emotions[emot]>EMOTION_MAX:
                emotions[emot] = EMOTION_MAX
             
        print(emotions)
        
        
        
        
def increase(to_increase, score):
    emotions[to_increase] += score
    
increase("joy", 2000)