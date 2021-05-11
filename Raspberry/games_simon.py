"""All the code has to be implemented with the music and buttons"""

import jsonhandler
import json
import random
import time

int i = 0
int prevled = 4
bool flag = True

"""Game of light to introduce the main game"""
def loop():
    global i, prevled
    
    for i in range(10):
        int r = random.randint(0,3)
        while prevled == r:
            r = random.randint(0,3)
        if r == 0:
            jsonhandler.send({"led":[r, [0,1,2]]})                                         """Led switch on with what colour?"""
            jsonhandler.send({"led":[1, 2, 3, [0,1,2], [0,1,2], [0,1,2]]})                 """Other leds switched off (?)"""
        if r == 1:
            jsonhandler.send({"led":[r, [0,1,2]]})                                         """Led switch on with what colour?"""
            jsonhandler.send({"led":[0, 2, 3, [0,1,2], [0,1,2], [0,1,2]]})                 """Other leds switched off (?)"""
        if r == 2:
            jsonhandler.send({"led":[r, [0,1,2]]})                                         """Led switch on with what colour?"""
            jsonhandler.send({"led":[0, 1, 3, [0,1,2], [0,1,2], [0,1,2]]})                 """Other leds switched off (?)"""
        if r == 3:
            jsonhandler.send({"led":[r, [0,1,2]]})                                         """Led switch on with what colour?"""
            jsonhandler.send({"led":[0, 1, 2, [0,1,2], [0,1,2], [0,1,2]]})                 """Other leds switched off (?)"""
        prevled = r
        time.sleep(0.1)



    """3...2...1...GO! (to implement)"""


    """Game started"""
    bool flag = True
    while flag == True:
        
        
        """start condition: keep number by the list of switched on Leds (to implement)"""
        
        
        """new led for the list"""
        r = random.randint(0,3)
        if r == 0:
            jsonhandler.send({"led":[r, [0,1,2]]})                                         """Led switch on with what colour?"""
            jsonhandler.send({"led":[1, 2, 3, [0,1,2], [0,1,2], [0,1,2]]})                 """Other leds switched off (?)"""
        if r == 1:
            jsonhandler.send({"led":[r, [0,1,2]]})                                         """Led switch on with what colour?"""
            jsonhandler.send({"led":[0, 2, 3, [0,1,2], [0,1,2], [0,1,2]]})                 """Other leds switched off (?)"""
        if r == 2:
            jsonhandler.send({"led":[r, [0,1,2]]})                                         """Led switch on with what colour?"""
            jsonhandler.send({"led":[0, 1, 3, [0,1,2], [0,1,2], [0,1,2]]})                 """Other leds switched off (?)"""
        if r == 3:
            jsonhandler.send({"led":[r, [0,1,2]]})                                         """Led switch on with what colour?"""
            jsonhandler.send({"led":[0, 1, 2, [0,1,2], [0,1,2], [0,1,2]]})                 """Other leds switched off (?)"""


        """update the list (to implement)"""


        if """button is wrong""" :
            flag = False                                                                       """end of the game"""