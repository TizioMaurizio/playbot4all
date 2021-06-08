import jsonhandler
import keyboard
import random
import time
import pygame
#import winsound
from threading import Thread
# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init()

#y starts the game
p='0'
buttonValues = [0, 0, 0, 0]
GAME_TICK = 1
prevtime = 0
playing = False
move_up_sound = pygame.mixer.Sound("Pop.wav")
def play_sound():
    global playing
    if not playing:
        playing = True
        move_up_sound.play()
        #winsound.PlaySound("Pop", winsound.SND_ALIAS)
        playing = False


def loop():
    global p, prevtime, playing, buttonValues

    currtime = time.time()
    try:
        if keyboard.is_pressed('y') and p != 'y':
            p = 'y'
            thread = Thread(target=play_sound)
            thread.start()
            jsonhandler.send({"rgb": [0,0,0]})
            print("Start catch the bug")
            playing = True
            
        if playing:
            thread = Thread(target=play_sound)
            if keyboard.is_pressed('u'):# or jsonhandler.getPlaybot()["button"][3]:#ORDINE INVERTITO##########################################################
                if jsonhandler.getPlaybot()["led"][0] == 1:
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            if keyboard.is_pressed('i'):# or jsonhandler.getPlaybot()["button"][2]:
                if jsonhandler.getPlaybot()["led"][1] == 1:
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            if keyboard.is_pressed('o'):# or jsonhandler.getPlaybot()["button"][1]:
                if jsonhandler.getPlaybot()["led"][2] == 1:
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            if keyboard.is_pressed('p'):# or jsonhandler.getPlaybot()["button"][0]:
                if jsonhandler.getPlaybot()["led"][3] == 1:
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            #if keyboard.is_pressed('i') and p != 'i':
                #p = 'u'
                #jsonhandler.send({"led":[0,0,0,0],"rgb":[[255,255,255],[4,5,6]]})

            if (currtime - prevtime > GAME_TICK):
                bug = round(random.random()*40)%4
                ledValues = [0,0,0,0,0,0,0,0]
                for i in range(4):
                    if i == bug:
                        ledValues[i] = 1
                    else:
                        ledValues[i] = 0
                jsonhandler.send({"led": ledValues,"button": buttonValues})
                prevtime = currtime
                print(ledValues)
    except:
        p = 0
        print("catchbug exception")
