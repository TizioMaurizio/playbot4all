import jsonhandler
import locomotion
import games
from jsonhandler import playbot
import keyboard

while True:
    try:
        print("ciao")
        jsonhandler.loop()
        locomotion.loop()
        #chatbot.loop()
        games.loop()
    except:
        print("exception")