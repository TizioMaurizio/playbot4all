import pygame
from pygame import mixer
import keyboard
import time

pygame.init()
pygame.mixer.init()

music = ["UnVeroAmicoInMe.wav", "GIORGIA_CREDO.wav", "Toploader_DancingintheMoonlight.wav" ]
nbSongs = 3
songID = 0
playing = False
status = False
pygame.mixer.music.load(music[songID])


while True:  
    try:  
        if keyboard.is_pressed('p') and not playing :
            playing =True
            time.sleep(0.3)
            print ("stopped->playing")
            print (songID)
            print (music[songID])
            pygame.mixer.music.play()
            
        #pygame.mixer.music.get_busy()--> Returns True when the music stream is actively playing. When the music is idle this returns False.
        if playing and pygame.mixer.music.get_busy() == False:
            break
    
        if keyboard.is_pressed('p')  and playing  :
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
                break

            pygame.mixer.music.load(music[songID])
            pygame.mixer.music.play()
            

    except:
        break 