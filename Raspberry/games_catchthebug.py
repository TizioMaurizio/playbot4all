 import jsonhandler
import keyboard
import random
import time
#y starts the game
p='0'
GAME_TICK = 1
prevtime = 0
playing = False

def loop():
    global p, prevtime, playing

    currtime = time.time()

    try:
        if keyboard.is_pressed('y') and p != 'u':
            print("Start catch the bug")
            playing = True
        if playing:
            if keyboard.is_pressed('u') and p != 'u':
                p = 'u'
                if jsonhandler.getPlaybot()["led"][0] == 1:
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    p = 0
            if keyboard.is_pressed('i') and p != 'i':
                p = 'i'
                if jsonhandler.getPlaybot()["led"][1] == 1:
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    p = 0
            if keyboard.is_pressed('o') and p != 'o':
                p = 'o'
                if jsonhandler.getPlaybot()["led"][2] == 1:
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    p = 0
            if keyboard.is_pressed('p') and p != 'p':
                p = 'p'
                if jsonhandler.getPlaybot()["led"][3] == 1:
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
                ledValues = [0,0,0,0]
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