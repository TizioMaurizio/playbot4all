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
playing = False



def loop():
    global playing, songID, nbSongs, music
    try:  
        if can_play("music") and not playing :
            status["music"] = True
            pygame.mixer.music.load(music[songID])
            playing =True
            time.sleep(0.3)
            print ("stopped->playing")
            print (songID)
            print (music[songID])
            pygame.mixer.music.play()
            
        #pygame.mixer.music.get_busy()--> Returns True when the music stream is actively playing. When the music is idle this returns False.
        if playing and pygame.mixer.music.get_busy() == False:
            status["music"] = False
    
        if can_play("music") and playing:
            status["music"] = True
            time.sleep(0.3)
            pygame.mixer.music.stop()
            print ("playing->stopped")
            songID += 1
            print (songID)
            print (music[songID])

            if songID == nbSongs:
                playing = False
                songID = 0
                pygame.mixer.music.stop()
                status["music"] = False

            pygame.mixer.music.load(music[songID])
            pygame.mixer.music.play()
            

    except Exception as e:
        print(e)
        traceback.print_exc()