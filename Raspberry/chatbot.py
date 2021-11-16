from chatbot_backend import Speak as Speak
from chatbot_backend import take_commands as take_commands
import jsonhandler
import serial

pressed = False
Speak("Ciao sono Pinguino")
def chatbot():
    global pressed
    if jsonhandler.getPlaybot()["button"][3] and not pressed:
        pressed = True
        #Speak("Ciao sono Pinguino")
        #Speak('Dimmi qualcosa!')
        command = take_commands()
        if "triste" in command:
            #musichetta triste, led accesi??
            Speak("Oh noo, come mai?")
        if "felice" in command:
                Speak("Sono felice anche io!")
        
        if "giochiamo" in command or "giocare" in command:
                Speak("A cosa vuoi giocare?")
                Speak("Premi martello per Catch the Bug")
                Speak("Premi nota musicale per ascoltare la musica")
                Speak("Premi piede per camminare")
                Speak("Premi microfono per parlare")
        else:
            pass
        command = ""
    elif not jsonhandler.getPlaybot()["button"][3]:
        pressed = False
    #Speak("Dimmi qualcosa...")
    #usare if per far partire giochi o dare comandi camminata?
    
