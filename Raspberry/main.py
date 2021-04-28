import jsonhandler
import locomotion
from jsonhandler import playbot
import keyboard

jsonhandler.send({"led":{"0":5,"1":5,"2":5,"3":5}})
jsonhandler.send({"servo":{"0":5,"1":5,"2":5,"3":5}})

while True:
    jsonhandler.loop()
    locomotion.loop()
    
            #print('send led')
    #print(playbot())