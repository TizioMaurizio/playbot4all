from chatbot_backend import Speak as Speak
from chatbot_backend import take_commands as take_commands

Speak("Ciao sono Pinguino")
def chatbot():
    command = take_commands()
    if "triste" in command:
        #musichetta triste, led accesi??
        Speak("Oh noo, come mai?")
        break
    if "felice" in command:
        Speak("Sono felice anche io!")
        break
    if "giochiamo" or "giocare" in command:
        Speak("A cosa vuoi giocare?")
        Speak("Premi martello per Catch the Bug")
        Speak("Premi nota musicale per ascoltare la musica")
        Speak("Premi piede per camminare")
        Speak("Premi microfono per parlare")
    #Speak("Dimmi qualcosa...")
    #usare if per far partire giochi o dare comandi camminata?
    
