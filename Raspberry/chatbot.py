"""
-Manages the speaker and the microphone interaction with raspberry
-Contains chatbot to reply to voice messages
-Selects locomotion states upon receiving movement commands
-Starts games upon receiving commands

INPUTS: message from microphone, robot pose (lying down, hit a wall, hugged)

OUTPUTS: voice message to speaker, walk direction/state (locomotion), selected game (games), 
"""