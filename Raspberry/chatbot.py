from chatbot_backend import Speak as Speak
from chatbot_backend import take_commands as take_commands
import jsonhandler
import serial
import time
from status import status as status
from status import can_play as can_play
import traceback

pressed = False
error = None

Speak("Ciao sono Pinguino")
def chatbot():
    global pressed, status, error
    
    if not pressed and can_play("chatbot"):
        status["chatbot"] = True
        pressed = True
        #Speak("Ciao sono Pinguino")
        #Speak('Dimmi qualcosa!')
    
        command = take_commands()
        error = command["error"]
        
        if "triste" in command["transcription"]:
            #musichetta triste, led accesi??
            Speak("Oh noo, mi dispiace. Per quel che vale, io ti voglio bene!")
            
            
        if "felice" in command["transcription"]:
            Speak("Wow, che grinta! Sono felice anche io.")
            
            
        if "cattura la pulce" in command["transcription"]:
            Speak("Giochiamo a cattura la pulce!")
            time.sleep(1)
            status["catchthebug"] = "startedbychatbot" ##DA SISEMARE
            
            
        if "giochi" in command["transcription"] or "giocare" in command["transcription"] or "giochiamo" in command["transcription"]:
            Speak("A cosa vuoi giocare?")
            Speak("Premi martello per cattura la pulce")
            Speak("Premi nota musicale per ascoltare la musica")
            Speak("Premi piede per camminare")
            Speak("Premi microfono per parlare")
            
        
        if "joystick" in command["transcription"]:
            Speak("Giochiamo insieme con il joystick a seguire le luci!")
            status["simon"] == "startedbychatbot"
            
                
            
        else:
            pass
        command["transcription"] = ""
            
        status["chatbot"] = False
        
    elif not (jsonhandler.getPlaybot()["button"][3]):
        pressed = False
    try:
        if error:# == "API unavailable" or command["error"] == "Unable to recognize speech":
            status["chatbot"] = False
    except:
        pass
        #traceback.print_exc()
    #print(pressed)
    #Speak("Dimmi qualcosa...")
    #usare if per far partire giochi o dare comandi camminata?      
