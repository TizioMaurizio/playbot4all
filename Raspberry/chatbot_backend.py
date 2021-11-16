# Importing required modules
# importing pyttsx3
import pyttsx3
#importing speech_recognition
import speech_recognition as sr
import jsonhandler

# creating Speak() function to giving Speaking power
# to our voice assistant
def Speak(audio):
    # initializing pyttsx3 module
    engine = pyttsx3.init()
    voice_id = 'italian'
    engine.setProperty('voice', voice_id)
    # anything we pass inside engine.say(),
    # will be spoken by our voice assistant
    engine.say(audio)
    engine.runAndWait()
#creating take_commands() function which
# can take some audio, Recognize and return
# if there are not any errors
def take_commands(): #PARTE QUANDO SI PREME MICROFONO (pulsante C)
    # initializing speech_recognition
    r = sr.Recognizer()
    # opening physical microphone of computer
    with sr.Microphone() as source:
        words = ['Ascolto...', 'Dimmi...']
        import random
        toSpeak = int(random.randrange(0,len(words)))
        print(words)
        print(toSpeak)
        Speak(words[toSpeak])
        r.adjust_for_ambient_noise(source)
        
        print(words[toSpeak])
        r.pause_threshold = 0.7
        # TURN ON RECORDING LED "C"
        # storing audio/sound to audio variable
        import time
        time.sleep(1)
        audio = r.listen(source)
        # TURN OFF RECORDING LED "C"
        try:
            Speak("Aspetta un attimo, sto cercando di capire cosa hai detto")
            print("Riconoscimento")
            # Recognizing audio using google api
            Query = r.recognize_google(audio, language="it-IT")
            print("Hai detto =\n", Query)
            Speak("Hai detto\n"+ Query)
        #SISTEMARE
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
            Speak("Non sono connesso a internet! Non posso parlare!") 
            
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"
        """except Exception as e:
            print(e)
            print("Prova a ripetere")
            Speak("Non ho capito, prova a ripetere")
            # returning none if there are errors
            return "None" """
    # returning audio as text
    import time
    time.sleep(1)
    return Query