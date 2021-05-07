import jsonhandler
import locomotion
import games
from jsonhandler import playbot
import keyboard

while True:
    try:
<<<<<<< HEAD
        print("ciao")
=======
>>>>>>> f0a500e67c561e41f0de66e15c1d3d69d07d85f4
        jsonhandler.loop()
        locomotion.loop()
        #chatbot.loop()
        games.loop()
    except:
        print("exception")