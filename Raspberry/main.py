from pbdebug import debug as debug
import jsonhandler
debug("jsonhandler imported")
import locomotion
debug("locomotion imported")
import chatbot
debug("chatbot imported")
import games
debug("games imported")
from jsonhandler import playbot
import traceback
import emotions
import time

while True:
    try:
        jsonhandler.loop()
        #locomotion.loop()
        chatbot.chatbot()
        games.loop()
        #emotions.loop()


    except:# RuntimeError: #TODO CHECK BETTER BECAUSE IT'S USEFUL
        traceback.print_exc()