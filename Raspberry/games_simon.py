"""All the code has to be implemented with the music and buttons"""

from serial.serialwin32 import Serial
import jsonhandler
import random
import time
import keyboard
import pygame
from threading import Thread

pygame.mixer.init()

pygame.init()

get_simon_sound = pygame.mixer.Sound("Pop.wav")
ready_sound = pygame.mixer.Sound("Ready-set-go")
up_led_sound = pygame.mixer.Sound("up_sound")
right_led_sound = pygame.mixer.Sound("right_sound")
down_led_sound = pygame.mixer.Sound("down_sound")
left_led_sound = pygame.mixer.Sound("left_sound")
win_sound = pygame.mixer.Sound("trumpet-win-super")
lose_sound = pygame.mixer.Sound("negative-beeps(lost)")




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
prevtime = 0
prevtime_2 = 0
ledValues = [0,0,0,0,0,0,0,0]
ledList = [0,0,0,0,0,0,0,0,0,0]
go = False
set = False
end_turn = False
flag = 0
LIGHTS_CLOCK = 0.2
WIN = 10
LOSE = 20

def play_sound():
    #get_simon_sound.play()
    if ledValues == [0,0,0,0,1,0,0,0]:
        up_led_sound.play()
    if ledValues == [0,0,0,0,0,1,0,0]:
        right_led_sound.play()
    if ledValues == [0,0,0,0,0,0,1,0]:
        down_led_sound.play()
    if ledValues == [0,0,0,0,0,0,0,1]:
        left_led_sound.play()
    if ledList[l-k] == 4:
        up_led_sound.play()
    if ledList[l-k] == 5:
        right_led_sound.play()
    if ledList[l-k] == 6:
        down_led_sound.play()
    if ledList[l-k] == 7:
        left_led_sound.play()
    if set == True:
        ready_sound.play()
    if k == WIN:
        win_sound.play()
    if k == LOSE:
        lose_sound.play()

"""Game of light to introduce the main game"""
def loop(): 
    
    global prevled, ready, i, j, playing, prevtime, go, set, ledValues, ledList, k, l, end_turn, prevtime_2, flag
    try:
        if keyboard.is_pressed('x'):
            print("Start Simon")
            playing = True
        if playing == True:
            thread1 = Thread(target=play_sound)    
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
                thread1.start()

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
                thread1.start()

                #if (currtime - prevtime) >= 1 and i < 3:
                    #winsound.Beep(DO, 200)
                    #i += 1
                    #prevtime = currtime
                #if (currtime - prevtime) >= 1 and i == 3:
                    #winsound.Beep(DO*2, 300)
                
                prevtime = currtime
                set = False
                flag = 1


            """Game starts -GO""" #da fare/completare
            if go == True and set == False and i == 0:
                if (currtime - prevtime) >= 4: #time of ready-set-go
                    l = k
                    while end_turn == True:
                        currtime = time.time()
                        if (currtime - prevtime_2) >= 4:
                            #sound
                            k = LOSE
                            end_turn = False
                            break
                        if ledList[l-k] == 4 and jsonhandler.getPlaybot()["analogstick"][1] >= 600 and (l-k) < k:
                            thread1.start()
                            prevtime_2 = currtime
                            l += 1
                        if ledList[l-k] == 5 and jsonhandler.getPlaybot()["analogstick"][0] <= 400 and (l-k) < k:
                            thread1.start()
                            prevtime_2 = currtime
                            l += 1
                        if ledList[l-k] == 6 and jsonhandler.getPlaybot()["analogstick"][1] <= 400 and (l-k) < k:
                            thread1.start()
                            prevtime_2 = currtime
                            l += 1
                        if ledList[l-k] == 7 and jsonhandler.getPlaybot()["analogstick"][0] >= 600 and (l-k) < k:
                            thread1.start()
                            prevtime_2 = currtime
                            l += 1
                        if (l-k) >= k:
                            end_turn = False



                    if k == WIN:
                        #winsound.PlaySound('trumpet-win-super.wav', winsound.SND_FILENAME)
                        #sound
                        thread1.start()
                        playing = False

                    if k == LOSE:
                         #winsound.PlaySound('lose.wav', winsound.SND_FILENAME)
                        #sound
                        thread1.start()
                        playing = False
                        j = 0
                        i = 0
                        k = 0
                        l = 0
                        flag = 0
                        prevled = 4 
                        ready = True
                        playing = False
                        prevtime = 0
                        prevtime_2 = 0
                        ledValues = [0,0,0,0,0,0,0,0]
                        ledList = [0,0,0,0,0,0,0,0,0,0]
                        go = False
                        set = False
                        end_turn = False



                    #NUOVO TURNO
                    if k > 0 and k < 10:     
                        for i in range(k-1):
                            for j in range(4, 7, 1):
                                if j == ledList[i]:
                                    ledValues[j] = 1
                                else:
                                    ledValues[j] = 0
                            jsonhandler.send({"led": ledValues})
                            thread1.start()
                            for j in range(10000):
                                j = j

                    if k < 10 and flag == 1:    
                        r = random.randint(4,7)
                        for j in range(4, 7, 1):
                            if j == r:
                                ledValues[j] = 1
                            else:
                                ledValues[j] = 0
                        jsonhandler.send({"led": ledValues})
                        thread1.start()
                        
                       
                        prevtime_2 = currtime
                        end_turn = True                        
                        ledList[k] = r
                        k += 1
                        ledValues = [0,0,0,0,0,0,0,0]
                        jsonhandler.send({"led": ledValues})
                        i = 0



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
                    #prevtime = currtime

                    #for j in range(30):
                        #ledList[j] =


                #if (currtime - prevtime) >= LIGHTS_CLOCK and go == False:
                 #   ready = True
                  #  prevtime = currtime
                   # i += 1

    


    except:
        print("simon exception")


            