# Importing required modules
# importing pyttsx3
import pyttsx3
#importing speech_recognition
import speech_recognition as sr
import jsonhandler
import time

# creating Speak() function to giving Speaking power
# to our voice assistant
def Speak(audio):
    # initializing pyttsx3 module
    engine = pyttsx3.init()
    voice_id = 'italian'
    engine.setProperty('voice', voice_id)
    # anything we pass inside engine.say(),
    # will be spoken by our voice assistant
    engine.say("Ciao sono pinguino")
    engine.runAndWait()
#creating take_commands() function which
# can take some audio, Recognize and return
# if there are not any errors
def take_commands(): #PARTE QUANDO SI PREME MICROFONO (pulsante C)
    # initializing speech_recognition
    r = sr.Recognizer()
    # opening physical microphone of computer
    with sr.Microphone() as source:
        words = ['Hei dimmi', 'Sono in ascolto']
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
        time.sleep(2)
        audio = r.listen(source)
        # TURN OFF RECORDING LED "C"
        
        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }        
            
        try:
            Speak("Aspetta un attimo, sto cercando di capire")
            print("Riconoscimento")
            # Recognizing audio using google api
            response["transcription"] = r.recognize_google(audio, language="it-IT")
            print("Hai detto =\n", response["transcription"] )
            Speak("Hai detto\n"+ response["transcription"] )
        #SISTEMARE---QUANDO CHATBOT ENTRA NELL'ECCEZIONE PROBLEMA CON GLI STATI 
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["transcription"]= None
            response["success"] = False
            response["error"] = "API unavailable"
            Speak("Non sono connesso a internet! Non posso parlare!")
            time.sleep(2)
            
            
        except sr.UnknownValueError:
            # speech was unintelligible
            response["transcription"] = None 
            response["error"] = "Unable to recognize speech"
            Speak("Non ho capito cosa hai detto")
            time.sleep(1)
            
                
            """except Exception as e:
            print(e)
            print("Prova a ripetere")"""
            
            # returning none if there are errors
        """return "None" """
    # returning audio as text
    time.sleep(1)
    
    return response