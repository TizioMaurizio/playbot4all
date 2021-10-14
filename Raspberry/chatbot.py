    
# Importing required modules
# importing pyttsx3
import pyttsx3
#importing speech_recognition
import speech_recognition as sr

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
def take_commands():
    # initializing speech_recognition
    r = sr.Recognizer()
    # opening physical microphone of computer
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        Speak('Dimmi qualcosa!Ascolto...')
        print('Ascolto...')
        r.pause_threshold = 0.7
        # storing audio/sound to audio variable
        audio = r.listen(source)
        try:
            Speak("Aspetta un attimo, sto cercando di capire cosa hai detto")
            print("Riconoscimento")
            # Recognizing audio using google api
            Query = r.recognize_google(audio, language="it-IT")
            print("Hai detto =\n", Query)
            Speak("Hai detto\n"+ Query)
        except Exception as e:
            print(e)
            print("Prova a ripetere")
            Speak("Non ho capito, prova a ripetere")
            # returning none if there are errors
            return "None"
    # returning audio as text
    import time
    time.sleep(1)
    return Query

Speak("Ciao sono Pinguino")
while True:
    command = take_commands() 
    if "triste" in command:
        #musichetta triste, led accesi??
        Speak("Oh noo, come mai?")
        break
    if "felice" in command:
        Speak("Sono felice anche io!")
        break
    #Speak("Dimmi qualcosa...")
    #usare if per far partire giochi o dare comandi camminata?