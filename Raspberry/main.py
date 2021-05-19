import jsonhandler
import locomotion
import games
from jsonhandler import playbot
import keyboard
import traceback
<<<<<<< HEAD
import emotions
=======

import emotions

>>>>>>> 3564d0c23661ab2c6e03c25afe3ad8abe777ddbd

while True:
    try:
        jsonhandler.loop()
        locomotion.loop()
        #chatbot.loop()
        games.loop()
<<<<<<< HEAD
        #emotions.loop()
=======

        emotions.loop()

        #emotions.loop()

>>>>>>> 3564d0c23661ab2c6e03c25afe3ad8abe777ddbd
    except:
        print("exception")