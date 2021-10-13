"""
-Manages the speaker and the microphone interaction with raspberry
-Contains chatbot to reply to voice messages
-Selects locomotion states upon receiving movement commands
-Starts games upon receiving commands

INPUTS: message from microphone, robot pose (lying down, hit a wall, hugged)

OUTPUTS: voice message to speaker, walk direction/state (locomotion), selected game (games), 
"""

""" text to speech offline  """

import time

import speech_recognition as sr
import pyttsx3
# Import the required module for text 
# to speech conversion
from gtts import gTTS 
from pygame import mixer

engine = pyttsx3.init() 
mixer.init()

# Language in which you want to convert (text to speech with gTTS google)
language = 'it'  #put 'it' to speak in italian

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
        engine.say("Non sono connesso a internet! Non posso parlare!") 
        engine.runAndWait()
        time.sleep(3)
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response



RANGE = 3
PROMPT_LIMIT=3
recognizer = sr.Recognizer()
microphone = sr.Microphone()

for i in range(PROMPT_LIMIT):
    
    for j in range(RANGE):

    
        mytext = "Ciao, sono Pinguino. Dimmi qualcosa!"
        myobj = gTTS(text=mytext, lang=language, slow=False)
        
        myobj.save("Ciao.mp3")
        print("File salvato!")
        # Playing the converted file
        mixer.music.load('Ciao.mp3')
        mixer.music.play()
        time.sleep(4)

        guess = recognize_speech_from_mic(recognizer, microphone)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        
        print("I didn't catch that. What did you say?\n")
        mytext = "Non ho capito. Cosa hai detto?"
        myobj = gTTS(text=mytext, lang=language, slow=False)
        
        myobj.save("Not_catch.mp3")
        print("File salvato!")
        # Playing the converted file
        mixer.music.load('Not_catch.mp3')
        mixer.music.play()
        time.sleep(4)
#         engine.say(mytext) 
#         engine.runAndWait()
#         time.sleep(3)

    # if there was an error, stop the game
    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))
        break

    # show the user the transcription
    print("You said: {}".format(guess["transcription"]))
    mytext= "Hai detto: {}".format(guess["transcription"])
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("you_said.mp3")
    print("File salvato!")
    # Playing the converted file
    mixer.music.load('you_said.mp3')
    mixer.music.play()
    time.sleep(6)


mytext = "Ciao,ciao. Alla prossima!"
myobj = gTTS(text=mytext, lang=language, slow=False)

myobj.save("Ciao1.mp3")
print("File salvato!")
# Playing the converted file
mixer.music.load('Ciao1.mp3')
mixer.music.play()
time.sleep(4)
