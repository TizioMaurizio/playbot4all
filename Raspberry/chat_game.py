import random
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
language = 'en'  #put 'it' to speak in italian


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


if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get a random word from the list
    word = random.choice(WORDS)

    # format the instructions string
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    mytext = instructions
    myobj = gTTS(text=mytext, lang=language, slow=False)
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save("instructions.mp3")
    print("File salvato!")
    # Playing the converted file
    mixer.music.load('instructions.mp3')
    mixer.music.play()
    time.sleep(13)

    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(i+1))
            mytext = 'Guess {}. Speak!'.format(i+1)
            engine.say(mytext) 
            engine.runAndWait()
            time.sleep(3)

            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")
            mytext = "I didn't catch that. What did you say?"
            myobj = gTTS(text=mytext, lang=language, slow=False)
    
            myobj.save("not_catch.mp3")
            print("File salvato!")
            # Playing the converted file
            mixer.music.load('not_chatch.mp3')
            mixer.music.play()
            time.sleep(3)

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))
        mytext= "You said: {}".format(guess["transcription"])
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("you_said.mp3")
        print("File salvato!")
        # Playing the converted file
        mixer.music.load('you_said.mp3')
        mixer.music.play()
        time.sleep(3)
        # determine if guess is correct and if any attempts remain
        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if guess_is_correct:
            print("Correct! You win!".format(word))
            mytext= "Correct! You win!".format(word)
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("Correct.mp3")
            print("File salvato!")
            # Playing the converted file
            mixer.music.load('Correct.mp3')
            mixer.music.play()
            time.sleep(3)
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
            mytext= "Incorrect. Try again."
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("Incorrect.mp3")
            print("File salvato!")
            # Playing the converted file
            mixer.music.load('Incorrect.mp3')
            mixer.music.play()
            time.sleep(3)
        else:
            print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            mytext= "Sorry, you lose!\nI was thinking of '{}'.".format(word)
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("Sorry.mp3")
            print("File salvato!")
            # Playing the converted file
            mixer.music.load('Sorry.mp3')
            mixer.music.play()
            time.sleep(3)
            break