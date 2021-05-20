"""All the code has to be implemented with the music and buttons"""

from serial.serialwin32 import Serial
import jsonhandler
import random
import time
import keyboard
import winsound
from threading import Thread

#class Suono (Thread):
    #def __init__(self, nome, durata):
      #Thread.__init__(self)
      #self.nome = nome
      #self.durata = durata
   #def run(self):
       


#thread1 = Suono("Thread#1", randint(1,100))
#thread2 = Suono("Thread#2", randint(1,100))
#thread3 = Suono("Thread#3", randint(1,100))


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


            """Game of lights -READY"""
            if ready == True:
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
                ready = False

            if i == 12:
                ledValues = [0,0,0,0,0,0,0,0]
                jsonhandler.send({"led": ledValues})
                ready = False
                go = True
                if (currtime - prevtime) >= LIGHTS_CLOCK+0.3:
                    set = True
                    i = 0


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
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            print(ledList[i])
                            #if ledList[i] == 4:
                                #winsound.Beep(DO, 500)
                            #if ledList[i] == 5:
                                #winsound.Beep(MI, 500)
                            #if ledList[i] == 6:
                                #winsound.Beep(SOL, 500)
                            #if ledList[i] == 7:
                                #winsound.Beep(SI, 500)




                        
                    r = random.randint(4,7)
                    for j in range(4, 7, 1):
                        if j == r:
                            ledValues[j] = 1
                        else:
                            ledValues[j] = 0
                    jsonhandler.send({"led": ledValues})
                    print("OKOKOKOKOK")
                    print("OKOKOKOKOK")
                    print("OKOKOKOKOK")
                    print("OKOKOKOKOK")
                    print(r)
                    print(r)
                    print(r)
                    print(r)
                    print(r)
                    #if r == 4:
                        #winsound.Beep(DO, 500)
                    #if r == 5:
                        #winsound.Beep(MI, 500)
                    #if r == 6:
                         #winsound.Beep(SOL, 500)
                    #if r == 7:
                        #winsound.Beep(SI, 500)
                    
                    #if (currtime - prevtime) >= 1:

                    
                    #if (currtime - prevtime) >= 0.5 and lights == True:



                    ledList[k] = r
                    k += 1
                    prevtime = currtime

                    if k >= 10:
                        winsound.PlaySound('trumpet-win-super.wav', winsound.SND_FILENAME)
                        playing = False

                    #for j in range(30):
                        #ledList[j] =


                #if (currtime - prevtime) >= LIGHTS_CLOCK and go == False:
                 #   ready = True
                  #  prevtime = currtime
                   # i += 1

    


    except:
        print("simon exception")


            