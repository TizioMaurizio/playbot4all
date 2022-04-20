"""All the code has to be implemented with the music and buttons"""

import jsonhandler
import random
import time
from status import status as status
#import keyboard
import pygame
from threading import Thread
import traceback

pygame.mixer.init()

pygame.init()

get_simon_sound = pygame.mixer.Sound(jsonhandler.path+"Pop.wav")
ready_sound = pygame.mixer.Sound(jsonhandler.path+"Ready-set-go.wav")
up_led_sound = pygame.mixer.Sound(jsonhandler.path+"up_sound.wav")
right_led_sound = pygame.mixer.Sound(jsonhandler.path+"right_sound.wav")
down_led_sound = pygame.mixer.Sound(jsonhandler.path+"down_sound.wav")
left_led_sound = pygame.mixer.Sound(jsonhandler.path+"left_sound.wav")
win_sound = pygame.mixer.Sound(jsonhandler.path+"trumpet-win-super.wav")
lose_sound = pygame.mixer.Sound(jsonhandler.path+"negative-beeps(lost).wav")

#while True:
    #for event in pygame.event.get():
        #if event.type == QUIT:
            #pygame.quit()
            #sys.exit()


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
m = 0
ready = True
playing = False
prevtime = 0
prevtime_2 = 0
prevtime_3 = 0
ledValues = [0,0,0,0,0,0,0,0]
ledList = [0,0,0,0,0,0,0,0,0,0]
go = False
sets = True
end_turn = False
new_led_flag = 0
analog_flag = 0
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
    if sets == True:
        ready_sound.play()
    if k == WIN:
        win_sound.play()
    if k == LOSE:
        lose_sound.play()

"""Game of light to introduce the main game"""
def loop(): 
    
    global ready, i, j, playing, prevtime, go, sets, ledValues, ledList, k, l, end_turn, prevtime_2, new_led_flag, analog_flag, status, m, prevtime_3
    try:
        thread1 = Thread(target=play_sound)
        if (not playing and (jsonhandler.getPlaybot()["analog"]["pressed"]) and status["playbot"] == "free") or (not playing and status["simon"] == "startedbychatbot"):
            #status["simon"] = True
            print("Start Simon")
            playing = True
        if playing == True:   
            """the game is initialized"""
            currtime = time.time()

            """3...2...1...start! -SET"""
            if sets == True:
                thread1.start()

                #if (currtime - prevtime) >= 1 and i < 3:
                    #winsound.Beep(DO, 200)
                    #i += 1
                    #prevtime = currtime
                #if (currtime - prevtime) >= 1 and i == 3:
                    #winsound.Beep(DO*2, 300)
                
                prevtime = currtime
                sets = False
                go = True
                new_led_flag = 1


            """Game starts -GO""" #da fare/completare
            #PARTE GIOCATORE
            if go == True and sets == False:
                if (currtime - prevtime) >= 5: #time of ready-set-go
                    if end_turn == True and analog_flag == 1:
                        currtime = time.time()
                        if (l-k) < k:
                            if ledList[l-k] == 4 and jsonhandler.getPlaybot()["analog"]["x"] <= 200:
                                ledValues = [0,0,0,0,1,0,0,0]
                                jsonhandler.send({"led": ledValues})
                                thread1.start()
                                prevtime_2 = currtime
                                l += 1
                        
                        if (l-k) < k:
                            if ledList[l-k] == 5 and jsonhandler.getPlaybot()["analog"]["y"] >= 800:
                                ledValues = [0,0,0,0,0,1,0,0]
                                jsonhandler.send({"led": ledValues})
                                thread1.start()
                                prevtime_2 = currtime
                                l += 1

                        if (l-k) < k:
                            if ledList[l-k] == 6 and jsonhandler.getPlaybot()["analog"]["x"] >= 600:
                                ledValues = [0,0,0,0,0,0,1,0]
                                jsonhandler.send({"led": ledValues})
                                thread1.start()
                                prevtime_2 = currtime
                                l += 1
                                
                        if (l-k) < k:
                            if ledList[l-k] == 7 and jsonhandler.getPlaybot()["analog"]["y"] <= 200:
                                ledValues = [0,0,0,0,0,0,0,1]
                                jsonhandler.send({"led": ledValues}) 
                                thread1.start()
                                prevtime_2 = currtime
                                l += 1

                        if (l-k) >= k:
                            end_turn = False
                            analog_flag = 0
                        
                        if (currtime - prevtime_2) >= 4:
                            #sound
                            k = LOSE
                            end_turn = False
                        
                        prevtime_3 = currtime



                    if k == WIN:
                        #winsound.PlaySound('trumpet-win-super.wav', winsound.SND_FILENAME)
                        #sound
                        thread1.start()
                        playing = False
                        j = 0
                        i = 0
                        k = 0
                        l = 0
                        new_led_flag = 0
                        analog_flag = 0
                        ready = True
                        prevtime = 0
                        prevtime_2 = 0
                        prevtime_3 = 0
                        ledValues = [0,0,0,0,0,0,0,0]
                        ledList = [0,0,0,0,0,0,0,0,0,0]
                        go = False
                        sets = False
                        end_turn = False
                        #status["simon"] = False

                    if k == LOSE:
                         #winsound.PlaySound('lose.wav', winsound.SND_FILENAME)
                        #sound
                        thread1.start()
                        playing = False
                        j = 0
                        i = 0
                        k = 0
                        l = 0
                        new_led_flag = 0
                        analog_flag = 0
                        ready = True
                        prevtime = 0
                        prevtime_2 = 0
                        prevtime_3 = 0
                        ledValues = [0,0,0,0,0,0,0,0]
                        ledList = [0,0,0,0,0,0,0,0,0,0]
                        go = False
                        sets = False
                        end_turn = False
                        #status["simon"] = False



                    #NUOVO TURNO
                    if k > 0 and k < 10 and new_led_flag == 0 and analog_flag == 0:     
                        if m < k and (currtime - prevtime_3) >= 1:
                            for j in range(4, 7, 1):
                                if j == ledList[m]:
                                    ledValues[j] = 1
                                else:
                                    ledValues[j] = 0
                            jsonhandler.send({"led": ledValues})
                            thread1.start()
                            m += 1
                        elif m >= k:
                            new_led_flag = 1
                        
                        #for i in range(k-1):
                           # for j in range(4, 7, 1):
                              #  if j == ledList[i]:
                              #      ledValues[j] = 1
                            #    else:
                             #       ledValues[j] = 0
                            #jsonhandler.send({"led": ledValues})
                           # thread1 = Thread(target=play_sound)
                           # thread1.start()
                            #for j in range(10000000):    #da cambiare
                             #   j = j
                            


                    if k < 10 and new_led_flag == 1 and analog_flag == 0:    
                        r = random.randint(4,7)
                        for j in range(4, 7, 1):
                            if j == r:
                                ledValues[j] = 1
                            else:
                                ledValues[j] = 0
                        jsonhandler.send({"led": ledValues})
                        thread1.start()
                        
                        currtime = time.time()
                        prevtime_2 = currtime
                        end_turn = True
                        analog_flag = 1                        
                        ledList[k] = r
                        k += 1
                        new_led_flag = 0
                        #ledValues = [0,0,0,0,0,0,0,0]
                        #jsonhandler.send({"led": ledValues})
                        l = k

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


            