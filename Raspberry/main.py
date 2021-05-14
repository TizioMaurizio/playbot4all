import jsonhandler
import locomotion
import games
import emotions
from jsonhandler import playbot
import keyboard
import traceback
import winsound

while True:
    try:
        jsonhandler.loop()
        locomotion.loop()
        #chatbot.loop()
        games.loop()
        emotions.loop()
        winsound.Beep(523, 1000)
    except:
        print("exception")
        traceback.print_exc()