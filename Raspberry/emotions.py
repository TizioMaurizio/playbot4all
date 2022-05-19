import jsonhandler
import time
import serial
import json
import traceback
from status import status
from threading import Thread
import pygame

pygame.mixer.init()

# Initialize pygame
pygame.init()
# example to increase an emotion: import emotions, emotions.increase("joy", 200): this will make the robot happy for at least 200 seconds
# every EMOTION_TICK seconds every emotion score is reduced by DELAY down to zero
happy_sound = pygame.mixer.Sound(jsonhandler.path+"procione.wav")
sound = happy_sound
playing_sound = False
def play_sound():
    global playing_sound
    if not playing_sound:
        playing_sound = True
        sound.play()
        #winsound.PlaySound("Pop", winsound.SND_ALIAS)
        playing_sound = False
        
thread = Thread(target=play_sound)
            
colors = {"anger": [255, 0, 0], "fear": [0, 255, 0], "sadness": [0, 0, 255], "joy": [255, 128, 0],
          "cyan": [0, 255, 255], "purple": [255, 0, 255], "white": [255, 255, 255]}
emotions = {"joy": 200, "anger": 120, "fear": 120, "sadness": 120}

DECAY = 1  # second
EMOTION_TICK = 1  # second
prevtime = 0
prevtime_rage = 0
EMOTION_MAX = 240  # maximum score for emotions
RAGE_THRESHOLD = 4
RAGE_TIME = 2
rage_pressed = 0
checking = False
buttons = [False, False, False, False, False, False, False, False]


# TODO
# blink when emotion score is very high
# smooth transition between colors
def emotion(emot):
    # todo emotion function, mind that import increases joy by 2000 as of now
    pass


def loop():
    global prevtime, prevtime_rage, rage_pressed, checking, RAGE_THRESHOLD, RAGE_TIME, thread, sound
    currtime = time.time()

    if (not checking):  # any button pressed
        for i in range(4):
            if jsonhandler.getPlaybot()["button"][i] == True:
                checking = True
                prevtime_rage = currtime
                rage_pressed = 0

    if checking:
        currtime_rage = time.time()
        for i in range(4):
            if jsonhandler.getPlaybot()["button"][i] == True:
                buttons[i] = True
            if not jsonhandler.getPlaybot()["button"][i] and buttons[i]:
                rage_pressed += 1
                buttons[i] = False

        if rage_pressed == RAGE_THRESHOLD:
            checking = False

        if currtime_rage - prevtime_rage > RAGE_TIME:
            checking = False
            rage_pressed = 0

    if (currtime - prevtime > EMOTION_TICK):
        prevtime = currtime
        current_emotion = max(emotions, key=emotions.get)  # choose the emotion with the maximum score
        if emotions[current_emotion] == 0:
            jsonhandler.send({"rgb": colors["fear"]})  # neutral is fear?
        else:
            send_color = colors[current_emotion]
            jsonhandler.send({"rgb": send_color})

        # increase FEAR when ir signals danger
        try:
            if jsonhandler.getPlaybot()["irsensor"][1] or not jsonhandler.getPlaybot()["irsensor"][2] or not \
            jsonhandler.getPlaybot()["irsensor"][0]:
                emotions["fear"] += 5
        except:
            print("no ir")
        # emotions["fear"] += 2

        # increase SADNESS when playbot is free
        try:
            if status["playbot"] != "free":
                emotions["sadness"] += 5
        except:
            print("no ir")
        # emotions["fear"] += 2

        # increase JOY with petting or playing
        try:
            if jsonhandler.getPlaybot()["capacitive"]:
                emotions["joy"] += 10
                sound = happy_sound
                play_sound()
            if status["playbot"] != "free":
                if emotions["joy"] < emotions["sadness"]:
                    emotions["joy"] = emotions["sadness"] + 10
                else:
                    emotions["joy"] += 10
            # TODO PLAY PETTING SOUND
        except:
            print("no capacitive")

        # increase ANGER if 4 buttons are pressed in less than 2 seconds
        try:
            if rage_pressed == RAGE_THRESHOLD:
                emotions["rage"] = 2000
                # TODO PLAY ANGER SOUND
        except:
            pass

        for emot in emotions:
            if emotions[emot] > 0:
                emotions[emot] -= DECAY
            if emotions[emot] > EMOTION_MAX:
                emotions[emot] = EMOTION_MAX

        #print(emotions)


def increase(to_increase, score):
    emotions[to_increase] += score
