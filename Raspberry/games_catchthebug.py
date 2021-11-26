import jsonhandler
#import keyboard
import random
import time
import pygame
from status import status as status
#import winsound
from threading import Thread
import traceback

from chatbot_backend import Speak as Speak
from chatbot_backend import take_commands as take_commands
# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init()

#y starts the game
p='0'
buttonValues = [0, 0, 0, 0]
GAME_TICK = 3
DIFFICULTY = 1.1
MAX_DIFFICULTY = 2
GAME_DURATION = 10
prevtime = 0
prevtime_begin = 0
playing_sound = False
playing_sound_begin = False
start_sound = pygame.mixer.Sound("yt1s.com-All-Vote-Out-Typing-Among-Us-Sound-Effect.wav")
pop_sound = pygame.mixer.Sound("Pop.wav")
#start_sound = pop_sound
defeat_sound = pygame.mixer.Sound("negative-beeps(lost).wav")
victory_sound = pygame.mixer.Sound("success-fanfare-trumpets.wav")
playing = False
taken = False
sending = False
progress = 0
score = 0
sound = pop_sound
starting = False

def play_sound():
    global playing_sound
    if not playing_sound:
        playing_sound = True
        sound.play()
        #winsound.PlaySound("Pop", winsound.SND_ALIAS)
        playing_sound = False
    
def play_sound_begin():
    global playing_sound_begin
    if not playing_sound:
        playing_sound_begin = True
        Speak("Cattura la pulce! Quando si illumina la pulce, premi il pulsante accanto per prenderla!")
        sound.play()
        time.sleep(10)
        #winsound.PlaySound("Pop", winsound.SND_ALIAS)
        playing_sound_begin = False


def loop():
    global p, prevtime, prevtime_begin, playing_sound, playing_sound_begin, buttonValues, playing, taken, sending, progress, score, GAME_TICK, DIFFICULTY, MAX_DIFFICULTY, sound, status, starting

    currtime = time.time()
    
    try:
        if (not playing and ((jsonhandler.getPlaybot()["button"][1]) and status["playbot"] == "free")) or (not playing and status["catchthebug"] == "startedbychatbot") or starting:
            
            if not starting:
                status["catchthebug"] = True
                prevtime_begin = time.time()
                starting = True
            p = 'y'
            #Speak("Cattura la pulce! Quando si illumina la pulce, premi il pulsante accanto per prenderla!")
            #ERRORE CON LA PARLATA
            
            if not playing_sound_begin:
                sound = start_sound
                thread = Thread(target=play_sound_begin)
                thread.start()
            #play_sound()
            if (currtime - prevtime_begin > 6):
                print("Start catch the bug")
                playing = True
                score = 0
                progress = 0
                starting = False
        
        if playing:
            #print(jsonhandler.getPlaybot())
            thread = Thread(target=play_sound)
            if jsonhandler.getPlaybot()["button"][0]:# or jsonhandler.getPlaybot()["button"][3]:#ORDINE INVERTITO##########################################################
                p = 'u'
                if (jsonhandler.getPlaybot()["led"][0] == 1) and not taken:
                    taken = True
                    sending = True
                    sound = pop_sound
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            elif jsonhandler.getPlaybot()["button"][1]:# or jsonhandler.getPlaybot()["button"][2]:
                p = 'i'
                if (jsonhandler.getPlaybot()["led"][2] == 1) and not taken:
                    taken = True
                    sending = True
                    sound = pop_sound
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            elif jsonhandler.getPlaybot()["button"][2]:# or jsonhandler.getPlaybot()["button"][1]:
                p = 'o'
                if (jsonhandler.getPlaybot()["led"][3] == 1) and not taken:
                    taken = True
                    sending = True
                    sound = pop_sound
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            elif jsonhandler.getPlaybot()["button"][3]:# or jsonhandler.getPlaybot()["button"][0]:
                p = 'p'
                if (jsonhandler.getPlaybot()["led"][1] == 1) and not taken:
                    taken = True
                    sending = True
                    sound = pop_sound
                    thread.start()
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
                    print("PRESO")
            else:
                p = '0'
            #if keyboard.is_pressed('i') and p != 'i':
                #p = 'u'
                #jsonhandler.send({"led":[0,0,0,0],"rgb":[[255,255,255],[4,5,6]]})
            
            if progress > GAME_DURATION:
                playing = False
                print("FINE, score ", score)
                if(score > GAME_DURATION/2):
                    sound = victory_sound
                    thread.start()
                else:
                    sound = defeat_sound
                    thread.start()
                    
                jsonhandler.send({"led": [0,0,0,0,0,0,0,0]})
                status["catchthebug"] = False
                return
            
            if (currtime - prevtime > GAME_TICK):
                progress = progress + 1
                bug = round(random.random()*40)%4
                ledValues = [0,0,0,0,0,0,0,0]
                for i in range(4):
                    if i == bug:
                        ledValues[i] = 1
                    else:
                        ledValues[i] = 0
                #buttonValues = [False,False,True,True] #TODO FALSIFY BUTTONS ON ARDUINO
                jsonhandler.send({"led": ledValues})#,"button": buttonValues})
                jsonhandler.send({"button": [0,0,0,0]})
                if taken:
                    score = score + 1
                    GAME_TICK = GAME_TICK / DIFFICULTY
                elif DIFFICULTY <= MAX_DIFFICULTY:
                    GAME_TICK = GAME_TICK * DIFFICULTY
                taken = False
                sending = False
                prevtime = currtime
                print(ledValues)
                
            if taken and sending and jsonhandler.getPlaybot()["led"] != [0,0,0,0,0,0,0,0]:
                if progress == GAME_DURATION:
                    progress = progress + 1
                sending = False
                jsonhandler.send({"led": [0,0,0,0,0,0,0,0]})#, "button": [0,0,0,0]})
                jsonhandler.send({"button": [0,0,0,0]})#, )
        else:
            if (currtime - prevtime > GAME_TICK):
                if jsonhandler.getPlaybot()["led"] != [0,0,0,0,0,0,0,0]:
                    jsonhandler.send({"led": [0,0,0,0,0,0,0,0]})
                prevtime = currtime
            
    except Exception as e:
        print(e)
        p = 0
        traceback.print_exc()
