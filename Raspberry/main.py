import jsonhandler
import locomotion
import games
from jsonhandler import playbot
import keyboard

while True:
    jsonhandler.loop()
    locomotion.loop()
    #chatbot.loop()
    games.loop()