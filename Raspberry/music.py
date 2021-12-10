import jsonhandler
import pygame
from pygame import mixer
import time
from status import status as status
from status import can_play as can_play
import traceback

pygame.init()
pygame.mixer.init()

music = ["UnVeroAmicoInMe.wav", "GIORGIA_CREDO.wav", "Toploader_DancingintheMoonlight.wav" ]
nbSongs = 3
songID = 0
x = False



def loop():
    global x, songID, nbSongs, music
    try:  
        if can_play("music") and not x :
            pygame.mixer.music.load(music[songID])
            status["music"] = True
            time.sleep(1)
            
            x =True
            
            print ("stopped->playing")
            print (songID)
            print (music[songID])
            pygame.mixer.music.play()
            
        #pygame.mixer.music.get_busy()--> Returns True when the music stream is actively playing. When the music is idle this returns False.
        if x and pygame.mixer.music.get_busy() == False:
            x = False
            status["music"] = False
    
        if jsonhandler.getPlaybot()["button"][2] and x:
            #status["music"] = True
            time.sleep(1)
            pygame.mixer.music.stop()
            print ("playing->stopped")
            songID += 1
            print (songID)
            print (music[songID])

            if songID == nbSongs:
                x = False
                songID = 0
                pygame.mixer.music.stop()
                status["music"] = False

            pygame.mixer.music.load(music[songID])
            pygame.mixer.music.play()
            

    except Exception as e:
        print(e)
        traceback.print_exc()