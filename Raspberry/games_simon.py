"""All the code has to be implemented with the music and buttons"""

from serial.serialwin32 import Serial
import jsonhandler
import random
import time
import keyboard
import winsound

<<<<<<< HEAD
=======

>>>>>>> 3564d0c23661ab2c6e03c25afe3ad8abe777ddbd
j = 0
i = 0
k = 0
l = 0
prevled = 4 
ready = True
playing = False
lights = True
prevtime = 0
ledValues = [0,0,0,0,0,0,0,0]
ledList = [0,0,0,0,0,0,0,0,0,0]
go = False
set = False

LIGHTS_CLOCK = 0.2
DO = 522 
MI = 658 
SOL = 784 
SI = 986


"""Game of light to introduce the main game"""
def loop():
    
    global prevled, ready, i, j, playing, prevtime, go, set, ledValues, ledList, k, l, lights
    
    try:
        if keyboard.is_pressed('x'):
            print("Start Simon")
            playing = True
        if playing == True:    
            """the game is initialized"""
            
            currtime = time.time()
<<<<<<< HEAD


            """Game of lights -READY"""
            if ready == True:
=======
            

            """Game of lights"""
            if first_start == True:
                ledValues = [0,0,0,0,0,0,0,0]

            """Game of lights -READY"""
            if ready == True:

>>>>>>> 3564d0c23661ab2c6e03c25afe3ad8abe777ddbd
                r = random.randint(4,7)
                for j in range(4, 7, 1):
                    if j == r:
                        ledValues[j] = 1
                    else:
                        ledValues[j] = 0
                jsonhandler.send({"led": ledValues})
                if r == 4:
                    winsound.Beep(DO, 50)
                if r == 5:
                    winsound.Beep(MI, 50)
                if r == 6:
                    winsound.Beep(SOL, 50)
                if r == 7:
                    winsound.Beep(SI, 50)
            if (currtime - prevtime) >= LIGHTS_CLOCK and go == False:
                ready = True
                prevtime = currtime
                i += 1
            else:
<<<<<<< HEAD
                ready = False
            if i == 12:
=======

                first_start = False
            if i == 12 and first_start == True:
                first_start = False
                next_start = True

                ready = False
            if i == 12:

>>>>>>> 3564d0c23661ab2c6e03c25afe3ad8abe777ddbd
                ledValues = [0,0,0,0,0,0,0,0]
                jsonhandler.send({"led": ledValues})
                ready = False
                go = True
                if (currtime - prevtime) >= LIGHTS_CLOCK+0.3:
                    set = True
                    i = 0


<<<<<<< HEAD
=======

            """3...2...1...GO! (to implement)"""
            

>>>>>>> 3564d0c23661ab2c6e03c25afe3ad8abe777ddbd
            """3...2...1...start! -SET"""
            if set == True:
                if (currtime - prevtime) >= 1 and i < 3:
                    winsound.Beep(DO, 200)
                    i += 1
                    prevtime = currtime
                if (currtime - prevtime) >= 1 and i == 3:
                    winsound.Beep(DO*2, 300)
                    set = False
                    prevtime = currtime


            """Game starts -GO""" #da fare/completare
            if go == True and set == False and i != 12:
                if (currtime - prevtime) >= 1:
                    if k > 0:     
                        for i in range(k-1):
                            for j in range(4, 7, 1):
                                if j == ledList[i]:
                                    ledValues[j] = 1
                                else:
                                    ledValues[j] = 0
                            jsonhandler.send({"led": ledValues})

                        
                    r = random.randint(4,7)
                    for j in range(4, 7, 1):
                        if j == r:
                            ledValues[j] = 1
                        else:
                            ledValues[j] = 0
                    jsonhandler.send({"led": ledValues})
                    
                    #if (currtime - prevtime) >= 0.5 and lights == True:



                    ledList[k] = r
                    k += 1
                    prevtime = currtime

                    if k >= 10:
                        playing = False

                    #for j in range(30):
                        #ledList[j] =


                #if (currtime - prevtime) >= LIGHTS_CLOCK and go == False:
                 #   ready = True
                  #  prevtime = currtime
                   # i += 1
<<<<<<< HEAD
=======

>>>>>>> 3564d0c23661ab2c6e03c25afe3ad8abe777ddbd





    except:
        print("simon exception")


            