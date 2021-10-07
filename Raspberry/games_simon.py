"""All the code has to be implemented with the music and buttons"""

import jsonhandler
import random
import time
import keyboard
import pygame
from threading import Thread
import traceback

pygame.mixer.init()

pygame.init()

get_simon_sound = pygame.mixer.Sound("Pop.wav")
ready_sound = pygame.mixer.Sound("Ready-set-go.wav")
up_led_sound = pygame.mixer.Sound("up_sound.wav")
right_led_sound = pygame.mixer.Sound("right_sound.wav")
down_led_sound = pygame.mixer.Sound("down_sound.wav")
left_led_sound = pygame.mixer.Sound("left_sound.wav")
win_sound = pygame.mixer.Sound("trumpet-win-super.wav")
lose_sound = pygame.mixer.Sound("negative-beeps(lost).wav")




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
set = True
end_turn = False
flag = 0
flag2 = 0
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
    #if ledList[l-k] == 4:
    #    up_led_sound.play()
    #if ledList[l-k] == 5:
    #    right_led_sound.play()
    #if ledList[l-k] == 6:
    #    down_led_sound.play()
    #if ledList[l-k] == 7:
    #    left_led_sound.play()
    if set == True:
        ready_sound.play()
    if k == WIN:
        win_sound.play()
    if k == LOSE:
        lose_sound.play()

"""Game of light to introduce the main game"""
def loop(): 
    
    global prevled, ready, i, j, playing, prevtime, go, set, ledValues, ledList, k, l, end_turn, prevtime_2, flag, flag2
    try:
        if keyboard.is_pressed('x'):
            print("Start Simon")
            playing = True
        if playing == True:
            thread1 = Thread(target=play_sound)    
            """the game is initialized"""
            currtime = time.time()
            

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
            if go == True and set == False:
                if (currtime - prevtime) >= 5: #time of ready-set-go
                    l = k
                    if end_turn == True and flag2 == 1:
                        currtime = time.time()
                        ledValues = [0,0,0,0,0,0,0,0]
                        jsonhandler.send({"led": ledValues})


                        while (currtime - prevtime_2) < 5:
                            currtime = time.time()
                            if ledList[l-k] == 4 and jsonhandler.getPlaybot()["analog"]["y"] >= 600 and (l-k) < k:
                                ledValues = [0,0,0,0,1,0,0,0]
                                jsonhandler.send({"led": ledValues})
                                thread1 = Thread(target=play_sound)
                                thread1.start()
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                l += 1
                            
                            if (l-k) >= k:
                                end_turn = False
                                flag2 = 0

                            if ledList[l-k] == 5 and jsonhandler.getPlaybot()["analog"]["x"] <= 1023 and (l-k) < k:
                                ledValues = [0,0,0,0,0,1,0,0]
                                jsonhandler.send({"led": ledValues})
                                thread1 = Thread(target=play_sound)
                                thread1.start()
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                l += 1
                            
                            if (l-k) >= k:
                                end_turn = False
                                flag2 = 0

                            if ledList[l-k] == 6 and jsonhandler.getPlaybot()["analog"]["y"] <= 400 and (l-k) < k:
                                ledValues = [0,0,0,0,0,0,1,0]
                                jsonhandler.send({"led": ledValues})
                                thread1 = Thread(target=play_sound)
                                thread1.start()
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                l += 1

                            if (l-k) >= k:
                                end_turn = False
                                flag2 = 0

                            if ledList[l-k] == 7 and jsonhandler.getPlaybot()["analog"]["x"] >= 600 and (l-k) < k:
                                ledValues = [0,0,0,0,0,0,0,1]
                                jsonhandler.send({"led": ledValues})
                                thread1 = Thread(target=play_sound)
                                thread1.start()
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                print(l, k)
                                l += 1
                            
                            if (l-k) >= k:
                                end_turn = False
                                flag2 = 0
                            
                            if (currtime - prevtime_2) >= 4:
                                #sound
                                k = LOSE
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
                        flag2 = 0
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
                    if k > 0 and k < 10 and flag2 == 0:     
                        for i in range(k-1):
                            for j in range(4, 7, 1):
                                if j == ledList[i]:
                                    ledValues[j] = 1
                                else:
                                    ledValues[j] = 0
                            jsonhandler.send({"led": ledValues})
                            thread1 = Thread(target=play_sound)
                            thread1.start()
                            for j in range(10000000):    #da cambiare
                                1 = 1

                    if k < 10 and flag == 1 and flag2 == 0:    
                        r = random.randint(4,7)
                        for j in range(4, 7, 1):
                            if j == r:
                                ledValues[j] = 1
                            else:
                                ledValues[j] = 0
                        jsonhandler.send({"led": ledValues})
                        thread1 = Thread(target=play_sound)
                        thread1.start()
                        
                       
                        prevtime_2 = currtime
                        end_turn = True
                        flag2 = 1                        
                        ledList[k] = r
                        k += 1
                        #ledValues = [0,0,0,0,0,0,0,0]
                        #jsonhandler.send({"led": ledValues})



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
        traceback.print_exc()


            