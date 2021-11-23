from pbdebug import debug as debug
import games_catchthebug
debug("games_catchthebug imported")
import games_simon
debug("games_simon imported")

p='0'
GAME_TICK = 3
prevtime = 0

def loop():
    games_catchthebug.loop() #start with key Y
    games_simon.loop() #start with key X