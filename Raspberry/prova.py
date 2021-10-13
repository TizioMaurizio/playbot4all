    
# Importing required modules
# importing pyttsx3
import pyttsx3
#importing speech_recognition
import speech_recognition as sr
# importing os module
import os
#creating take_commands() function which
# can take some audio, Recognize and return
# if there are not any errors
def take_commands():
    # initializing speech_recognition
    r = sr.Recognizer()
    # opening physical microphone of computer
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('Ascolto...')
        r.pause_threshold = 0.7
        # storing audio/sound to audio variable
        audio = r.listen(source)
        try:
            print("Riconoscimento")
            # Recognizing audio using google api
            Query = r.recognize_google(audio, language="it-IT")
            print("Hai detto =\n", Query)
        except Exception as e:
            print(e)
            print("Prova a ripetere")
            # returning none if there are errors
            return "None"
    # returning audio as text
    import time
    time.sleep(2)
    return Query
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
Speak("Vuoi spegnere il computer, Marco?")
while True:
    command = take_commands()
    if "no" in command:
        Speak("Ok Marco, lascio acceso")
        break
    if "yes" in command:
        # Shutting down
        Speak("Spengo")
        #os.system("shutdown -h now")
        break
    Speak("Puoi ripetere? grazie")