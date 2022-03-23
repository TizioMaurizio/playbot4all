import jsonhandler
import pygame
from pygame import mixer
import time
from status import status as status
from status import can_play as can_play
import traceback



from chatbot_backend import Speak as Speak
from chatbot_backend import take_commands as take_commands

pygame.init()
pygame.mixer.init()

#tempo partenza musica SISTEMARE

music = ["UnVeroAmicoInMe.wav", "GIORGIA_CREDO.wav", "Toploader_DancingintheMoonlight.wav", "Wheres_the_love.wav" ]
nbSongs = len(music)
songID = 0
playing = False
pressed = False
chatbot = False

def loop():
    global playing, pressed, songID, nbSongs, music, chatbot
    try:
        if not jsonhandler.getPlaybot()["button"][2]:
            pressed = False
            
        #print(pygame.mixer.music.get_busy())
        
        if status["music"] == "startedbychatbot":
            chatbot = True
                
        if can_play("music") and not playing :
            #Speak("un po' di musica! Ascolta la canzone fino alla fine oppure rischiaccia il bottone per cambiare")
            pygame.mixer.music.load(music[songID])
            status["music"] = True
            #time.sleep(1)
            Speak("un po' di musica! Ascolta la canzone fino alla fine oppure rischiaccia il bottone per cambiare")
            playing =True
            
            #print ("stopped->playing")
            #print (songID)
            #print (music[songID])
            pygame.mixer.music.play()
            if chatbot:
                songID += 1
                if songID > nbSongs:
                    playing = False
                    pygame.mixer.music.stop()
                    status["music"] = False
                    songID = 0
        #Music finished
        #pygame.mixer.music.get_busy()--> Returns True when the music stream is actively playing. When the music is idle this returns False.
        if playing and (pygame.mixer.music.get_busy() == False):
            playing = False
            status["music"] = False
            songID = 0
    
        #Play next music (leave if last music)
        if jsonhandler.getPlaybot()["button"][2] and status["playbot"] == "busy" and not pressed and playing:
            pressed = True
            status["music"] = True
            time.sleep(0.2)
            pygame.mixer.music.stop()
            print ("playing->stopped")  
            pygame.mixer.music.load(music[songID])
            pygame.mixer.music.play()
            songID += 1 
            #print (songID)
            #print (music[songID])

            if songID > nbSongs:
                playing = False
                pygame.mixer.music.stop()
                status["music"] = False
                songID = 0
                
            chatbot = False 

            

    except Exception as e:
        print(e)
        songID = 0
        pressed = False
        traceback.print_exc()