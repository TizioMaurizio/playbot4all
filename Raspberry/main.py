import jsonhandler
import locomotion
import games
from jsonhandler import playbot
import keyboard
<<<<<<< HEAD
import traceback
=======
import emotions
>>>>>>> 98678b8a1799d28b7b529119aace59123d6d8544

while True:
    try:
        jsonhandler.loop()
        locomotion.loop()
        #chatbot.loop()
        games.loop()
<<<<<<< HEAD
        emotions.loop()
=======
        #emotions.loop()
>>>>>>> 98678b8a1799d28b7b529119aace59123d6d8544
    except:
        print("exception")