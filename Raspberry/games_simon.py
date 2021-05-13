"""All the code has to be implemented with the music and buttons"""

import jsonhandler
import random
import time
import keyboard

j = 0
i = 0
prevled = 4
first_start = True
playing = False
prevtime = 0
LIGHTS_CLOCK = 0.2
next_start = False


"""Game of light to introduce the main game"""
def loop():
    
    global prevled, first_start, i, j, playing, prevtime, next_start
    
    try:
        if keyboard.is_pressed('x'):
            print("Start Simon")
            playing = True
        if playing == True:    
            """the game is initialized"""
            
            currtime = time.time()
            
            """Game of lights"""
            if first_start == True:
                ledValues = [0,0,0,0,0,0,0,0]
                r = random.randint(4,7)
                for j in range(4, 7, 1):
                    if j == r:
                        ledValues[j] = 1
                    else:
                        ledValues[j] = 0
                jsonhandler.send({"led": ledValues})
            if (currtime - prevtime) >= LIGHTS_CLOCK and next_start == False:
                first_start = True
                prevtime = currtime
                i += 1
            else:
                first_start = False
            if i == 12 and first_start == True:
                first_start = False
                next_start = True
                ledValues = [0,0,0,0,0,0,0,0]
                jsonhandler.send({"led": ledValues})
            


            """3...2...1...GO! (to implement)"""


            """Game starts"""
            if next_start == True:
                r = random.randint(4,7)
                for j in range(4, 7, 1):
                    if j == r:
                        ledValues[j] = 1
                    else:
                        ledValues[j] = 0
                jsonhandler.send({"led": ledValues})
            if (currtime - prevtime) >= LIGHTS_CLOCK and next_start == False:
                first_start = True
                prevtime = currtime
                i += 1
            else:
                first_start = False






    except:
        print("simon exception")


            