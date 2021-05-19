import jsonhandler
import locomotion
import games
from jsonhandler import playbot
import keyboard
import emotions

while True:
    try:
        jsonhandler.loop()
        locomotion.loop()
        #chatbot.loop()
        games.loop()
        #emotions.loop()
    except:
        print("exception")