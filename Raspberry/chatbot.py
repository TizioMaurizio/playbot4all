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

        if "ciao" in command["transcription"]:
            Speak("Ciao")

        if "buongiorno" in command["transcription"]:
            Speak("buongiorno a te")

        if "specchio riflesso" in command["transcription"]:
            Speak("oihcceps osselfir")

        if "buonasera" in command["transcription"]:
            Speak("buonasera a te")

        if "grazie" in command["transcription"]:
            Speak("figurati, sono felice di aiutarti")

        if "scusa" in command["transcription"] or "mi dispiace" in command["transcription"] or "scusami" in command["transcription"]:
            Speak("tranquilla")
        
        if "anni" in command["transcription"] or "età" in command["transcription"]:
            Speak("sono nato nel 2021")

        if "come stai" in command["transcription"]:
            Speak("Io sono felice. Tu come ti senti?")

        if "come ti senti" in command["transcription"]:
            Speak("Io sono felice. Tu come stai?")
        
        if "triste" in command["transcription"] or "arrabbiata" in command["transcription"] or "delusa" in command["transcription"]:
            #musichetta triste, led accesi??
            Speak("Oh noo, mi dispiace. Per quel che vale, io ti voglio bene!")
            
            
        if "felice" in command["transcription"] or "contento" in command["transcription"] or "sorridente" in command["transcription"]:
            Speak("Wow, che grinta! Sono felice anche io.")
            
            
        if "cattura" in command["transcription"] or "pulce" in command["transcription"] or "marmotta" in command["transcription"]:
            Speak("Giochiamo a cattura la pulce!")
            time.sleep(1)
            status["catchthebug"] = "startedbychatbot"
            
        if "musica" in command["transcription"] or "canzone" in command["transcription"] or "melodia" in command["transcription"] or "cantare" in command["transcription"] or "canto" in command["transcription"]:
            Speak("Diamoci dentro con un po' di musica!")
            #time.sleep(1)
            status["music"] = "startedbychatbot"
            
            
        if "giochi" in command["transcription"] or "giocare" in command["transcription"] or "giochiamo" in command["transcription"]:
            Speak("A cosa vuoi giocare?")
            Speak("Premi martello per cattura la pulce")
            Speak("Premi nota musicale per ascoltare la musica")
            Speak("Premi piede per camminare")
            Speak("Premi microfono per parlare")
            
        
        if "joystick" in command["transcription"]:
            Speak("Giochiamo insieme con il joystick a seguire le luci!")
            status["simon"] == "startedbychatbot"
            
        if "simon" in command["transcription"]:
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
