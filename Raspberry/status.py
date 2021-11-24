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
        status["playbot"] = "free"
    else:
        if not toFree:
            status["playbot"] = "busy"
    
    if (currtime - prevtime > 1) and toFree:
        
        toFree = False
    #CONTROLLARE TOFREE PERCHE RIMANE A BUSY CON TRUE    
    print(status["playbot"])
    print(toFree)


