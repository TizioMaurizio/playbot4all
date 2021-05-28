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
GAME_TICK = 1
prevtime = 0
playing = False
move_up_sound = pygame.mixer.Sound("Pop.wav")
def play_sound():
    move_up_sound.play()
    #winsound.PlaySound("Pop", winsound.SND_ALIAS)


def loop():
    global p, prevtime, playing

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
            if keyboard.is_pressed('u') and p != 'u' or jsonhandler.getPlaybot()["button"][3]:#ORDINE INVERTITO##########################################################
                p = 'u'
                if jsonhandler.getPlaybot()["led"][0] == 1:
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    p = 0
            if keyboard.is_pressed('i') and p != 'i' or jsonhandler.getPlaybot()["button"][2]:
                p = 'i'
                if jsonhandler.getPlaybot()["led"][1] == 1:
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    p = 0
            if keyboard.is_pressed('o') and p != 'o' or jsonhandler.getPlaybot()["button"][1]:
                p = 'o'
                if jsonhandler.getPlaybot()["led"][2] == 1:
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    p = 0
            if keyboard.is_pressed('p') and p != 'p' or jsonhandler.getPlaybot()["button"][0]:
                p = 'p'
                if jsonhandler.getPlaybot()["led"][3] == 1:
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    p = 0
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
                jsonhandler.send({"led": ledValues})
                prevtime = currtime
                print(ledValues)
    except:
        p = 0
        print("catchbug exception")
