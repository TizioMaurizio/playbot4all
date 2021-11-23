from chatbot_backend import Speak as Speak
from chatbot_backend import take_commands as take_commands
import jsonhandler
import serial
from status import status as status

pressed = False
Speak("Ciao sono Pinguino")
def chatbot():
    global pressed, status
    
    if not pressed and (jsonhandler.getPlaybot()["button"][3]) and status["playbot"] == "free":
        status["chatbot"] = True
        pressed = True
        #Speak("Ciao sono Pinguino")
        #Speak('Dimmi qualcosa!')
        command = take_commands()
        
        if "triste" in command:
            #musichetta triste, led accesi??
            Speak("Oh noo, come mai?")
            
        if "felice" in command:
            Speak("Sono felice anche io!")
            
        if "cattura la pulce" in command:
            Speak("Giochiamo a cattura la pulce!")
            status["catchthebug"] = "startedbychatbot"
            
        if "giochiamo" in command or "giocare" in command:
            Speak("A cosa vuoi giocare?")
            Speak("Premi martello per Catch the Bug")
            Speak("Premi nota musicale per ascoltare la musica")
            Speak("Premi piede per camminare")
            Speak("Premi microfono per parlare")
            
        else:
            pass
        command = ""
        status["chatbot"] = False
        
    elif not (jsonhandler.getPlaybot()["button"][3]):
        pressed = False
    
    #print(pressed)
    #Speak("Dimmi qualcosa...")
    #usare if per far partire giochi o dare comandi camminata?      
