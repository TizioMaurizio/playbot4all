import jsonhandler
import locomotion
import games
import emotions
from jsonhandler import playbot
import keyboard
import traceback

while True:
    try:
        jsonhandler.loop()
        locomotion.loop()
        #chatbot.loop()
        games.loop()
        emotions.loop()
    except:
        print("exception")
        traceback.print_exc()