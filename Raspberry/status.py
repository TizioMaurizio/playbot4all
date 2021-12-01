"""
import time
status = dict()
status["playbot"] = "free" #busy
status["catchthebug"] = False #True
status["simon"] = False
status["music"] = False
status["locomotion"] = False
status["chatbot"] = False
#games_status.status["nomegioco"] = "finished"
prevtime = 0
toFree = False
def loop():
    global status, prevtime, toFree
    currtime = time.time()
    check = -1 #status["playbot"] should never be False or empty
    for s in status:
        if status[s]:
            check = check + 1
    if check == 0:
        prevtime = time.time()
        toFree = True
        if (currtime - prevtime > 0.5):
            status["playbot"] = "free"
            toFree = False
    else:
        if not toFree:
            status["playbot"] = "busy"
        
    #print(status["playbot"])
"""
import jsonhandler
from pbdebug import debug as debug
import time
status = dict()
status["playbot"] = "free" #busy
status["catchthebug"] = False #True
status["simon"] = False
status["music"] = False
status["locomotion"] = False
status["chatbot"] = False
#games_status.status["nomegioco"] = "finished"
prevtime = 0
toFree = False
check_changed = False
prev_check = 0

def loop():
    global status, prevtime, toFree, prev_check
    currtime = time.time()
    check = -1 #status["playbot"] should never be False or empty
    for s in status:
        if status[s]:
            check = check + 1
    check_changed = not (prev_check == check)
    if check == 0 and check_changed:
        prevtime = time.time()
        toFree = True
    else:
        if check == 0:
            pass
        else:
            status["playbot"] = "busy"
            toFree = False
       #if not toFree:
            #status["playbot"] = "busy"
    #print(prevtime)
    #print(currtime)
    if (currtime - prevtime > 1) and toFree:
        status["playbot"] = "free"
        toFree = False
        
    prev_check = check
    #debug(status["playbot"])
    #debug(toFree)
#

def button(game):
    if game == "catchthebug":
        return 1
    if game == "chatbot":
        return 3
    if game == "locomotion":
        return 0
    if game == "music":
        return 2

def can_play(game):
    return (((jsonhandler.getPlaybot()["button"][button(game)]) and status["playbot"] == "free") or status[game] == "startedbychatbot")
