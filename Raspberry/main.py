from pbdebug import debug as debug
import jsonhandler
debug("jsonhandler imported")
import locomotion
debug("locomotion imported")
import chatbot
debug("chatbot imported")
import games
debug("games imported")
import music
from jsonhandler import playbot
import traceback
import emotions
import time
import status

while True:
    try:
        time.sleep(0.01)
        print("jsonhandler")
        jsonhandler.loop()
        print("locomotion")
        locomotion.loop()
        print("chatbot")
        chatbot.chatbot()
        print("games")
        games.loop()
        print("emotions")
        emotions.loop()
        print("music")
        music.loop()
        print("status")
        status.loop()


    except:# RuntimeError: #TODO CHECK BETTER BECAUSE IT'S USEFUL
        traceback.print_exc()