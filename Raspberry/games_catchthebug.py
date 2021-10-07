import jsonhandler
import keyboard
import random
import time
import pygame
#import winsound
from threading import Thread
import traceback
# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init()

#y starts the game
p='0'
buttonValues = [0, 0, 0, 0]
GAME_TICK = 3
DIFFICULTY = 1.5
GAME_DURATION = 20
prevtime = 0
playing_sound = False
move_up_sound = pygame.mixer.Sound("Pop.wav")
playing = False
taken = False
sending = False
progress = 0
score = 0

def play_sound():
    global playing_sound
    if not playing_sound:
        playing_sound = True
        move_up_sound.play()
        #winsound.PlaySound("Pop", winsound.SND_ALIAS)
        playing_sound = False


def loop():
    global p, prevtime, playing_sound, buttonValues, playing, taken, sending, progress, score, GAME_TICK, DIFFICULTY

    currtime = time.time()
    try:
        if keyboard.is_pressed('y') and not playing:
            p = 'y'
            thread = Thread(target=play_sound)
            thread.start()
            print("Start catch the bug")
            playing = True
            score = 0
            progress = 0
        
        if playing:
            #print(jsonhandler.getPlaybot())
            thread = Thread(target=play_sound)
            if keyboard.is_pressed('u') or jsonhandler.getPlaybot()["button"][3]:# or jsonhandler.getPlaybot()["button"][3]:#ORDINE INVERTITO##########################################################
                p = 'u'
                if (jsonhandler.getPlaybot()["led"][0] == 1) and not taken:
                    taken = True
                    sending = True
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            elif keyboard.is_pressed('i') or jsonhandler.getPlaybot()["button"][2]:# or jsonhandler.getPlaybot()["button"][2]:
                p = 'i'
                if (jsonhandler.getPlaybot()["led"][1] == 1) and not taken:
                    taken = True
                    sending = True
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            elif keyboard.is_pressed('o') or jsonhandler.getPlaybot()["button"][1]:# or jsonhandler.getPlaybot()["button"][1]:
                p = 'o'
                if (jsonhandler.getPlaybot()["led"][2] == 1) and not taken:
                    taken = True
                    sending = True
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            elif keyboard.is_pressed('p') or jsonhandler.getPlaybot()["button"][0]:# or jsonhandler.getPlaybot()["button"][0]:
                p = 'p'
                if (jsonhandler.getPlaybot()["led"][3] == 1) and not taken:
                    taken = True
                    sending = True
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            else:
                p = '0'
            #if keyboard.is_pressed('i') and p != 'i':
                #p = 'u'
                #jsonhandler.send({"led":[0,0,0,0],"rgb":[[255,255,255],[4,5,6]]})
            
            if progress > GAME_DURATION:
                playing = False
                print("FINE, score ", score)
                jsonhandler.send({"led": [0,0,0,0,0,0,0,0]})
                return
            
            if (currtime - prevtime > GAME_TICK):
                progress = progress + 1
                bug = round(random.random()*40)%4
                ledValues = [0,0,0,0,0,0,0,0]
                for i in range(4):
                    if i == bug:
                        ledValues[i] = 1
                    else:
                        ledValues[i] = 0
                #buttonValues = [False,False,True,True] #TODO FALSIFY BUTTONS ON ARDUINO
                jsonhandler.send({"led": ledValues})#,"button": buttonValues})
                if taken:
                    score = score + 1
                    GAME_TICK = GAME_TICK / DIFFICULTY
                else:
                    GAME_TICK = GAME_TICK * DIFFICULTY
                taken = False
                sending = False
                prevtime = currtime
                print(ledValues)
                
            if taken and sending and jsonhandler.getPlaybot()["led"] != [0,0,0,0,0,0,0,0]:
                sending = False
                jsonhandler.send({"led": [0,0,0,0,0,0,0,0]})#, "button": [0,0,0,0]})
                jsonhandler.send({"button": [0,0,0,0]})#, )
            
            
    except:
        p = 0
        traceback.print_exc()
