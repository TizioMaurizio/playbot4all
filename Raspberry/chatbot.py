"""
-Manages the speaker and the microphone interaction with raspberry
-Contains chatbot to reply to voice messages
-Selects locomotion states upon receiving movement commands
-Starts games upon receiving commands

INPUTS: message from microphone, robot pose (lying down, hit a wall, hugged)

OUTPUTS: voice message to speaker, walk direction/state (locomotion), selected game (games), 
"""

""" text to speech offline  """

import pyttsx3, time             #text to speech

#pip3 install pyttsx3
#apt-get install alsa-utils

engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice

#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[36].id)   #changing index, changes voices. 1 for female


#engine.say("Hi, say something!") 
engine.say("Ciao, sono pinguino. Dimmi qualcosa!")

engine.runAndWait()
