from pbdebug import debug as debug
import jsonhandler
debug("jsonhandler imported")
import locomotion
debug("locomotion imported")
import games
debug("games imported")
from jsonhandler import playbot
import traceback

import emotions


while True:
    try:
        jsonhandler.loop()
        locomotion.loop()
        #chatbot.loop()
        games.loop()
        #emotions.loop()


    except:
        traceback.print_exc()