import jsonhandler
import keyboard

def loop():
    if keyboard.is_pressed('p'):
        jsonhandler.send({"led":[0,1,[0,1,2],[0,1,2]]})