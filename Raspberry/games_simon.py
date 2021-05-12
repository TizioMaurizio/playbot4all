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


"""Game of light to introduce the main game"""
def loop():
    
    global prevled, first_start, i, j, playing
    
    try:
        if keyboard.is_pressed('x'):
            print("Start Simon")
            playing = True
        if playing == True:    
            if first_start == True:
                ledValues = [0,0,0,0]
                for i in range(10):
                    r = random.randint(0,3)
                    while prevled == r:
                        r = random.randint(0,3)
                    for j in range(4):
                        if j == r:
                            ledValues[j] = 1
                        else:
                            ledValues[j] = 0
                    jsonhandler.send({"led": ledValues})
                    prevled = r
                    time.sleep(0.1)
                first_start = False
            


            """3...2...1...GO! (to implement)"""


            """Game first_started"""
            if first_start == False:
                flag = 1
                while flag == 1:
                    
                    
                    """start condition: keep number by the list of switched on Leds (to implement)"""
                    
                    
                    """new led for the list"""
                    r = random.randint(0,3)
                    ledValues = [0,0,0,0]
                    while prevled == r:
                        r = random.randint(0,3)
                    for j in range(4):
                        if r == j:
                            ledValues[r] = 1
                        else:
                            ledValues[r] = 0
                    if r == 0:
                        jsonhandler.send({"led":ledValues})
                    if r == 1:
                        jsonhandler.send({"led":ledValues})
                    if r == 2:
                        jsonhandler.send({"led":ledValues})
                    if r == 3:
                        jsonhandler.send({"led":ledValues})


                    """update the list (to implement)"""


                    if """button is wrong""" :
                        flag = 0                                                                  |    """end of the game"""

    except:
        print("simon exception")


            