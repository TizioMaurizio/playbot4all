"""4wheelController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Keyboard
from controller import Motor, Brake, PositionSensor
import tkinter as tk
import threading
import time

# create the Robot instance.
robot = Robot()
window = tk.Tk()
greeting = tk.Label(text="Hello, Webots")
greeting.pack()

def remote():
    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())
    
    keyboard=Keyboard()
    keyboard.enable(timestep)
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  motor = robot.getMotor('motorname')
    #  ds = robot.getDistanceSensor('dsname')
    #  ds.enable(timestep)
    
    # initialize motors
    
    #ROBOT GAIT PARAMETERS
    #each of these variables defines the target angles for the gait
    #0.4, 0.15 tall robot, 0.4,0.3 short robot
    #THURST AND MAXIMUM LEAN ARE COUPLED, MINIMUM LEAN AND TURN ARE DECOUPLED
    AAA = 0.4
    BBB = 0.2
    CCC = -0.4
    DDD = -0.2
    TURNA = -0.5
    TURNB = 0.5
    ZERO = 0
    
    wheels = []
    jointNames = ['hip_right','leg_right','hip_left','leg_left']
    positionLimits = { 'leg_left': [AAA,DDD], 'leg_right': [BBB,CCC], 'hip_left': [AAA, CCC], 'hip_right': [AAA, CCC] }
    tolerance = 0.01
    joints = dict()
    
    def pos(joint):
        return joints[joint].getPositionSensor().getValue()
    completed = False
    
    def reach(positions,velocities):
           if complete(positions):
               return True
           else:
               velocity = 1
               joints['hip_right'].setPosition(positions[ZERO])
               joints['hip_right'].setVelocity(velocities[ZERO])
               joints['leg_right'].setPosition(positions[1])
               joints['leg_right'].setVelocity(velocities[1])
               joints['hip_left'].setPosition(positions[2])
               joints['hip_left'].setVelocity(velocities[2])
               joints['leg_left'].setPosition(positions[3])
               joints['leg_left'].setVelocity(velocities[3])
               return False
                   
    
    def complete(positions):
       for i in range(4):
           if(abs(abs(pos(jointNames[i])) - abs(positions[i])) > tolerance or pos(jointNames[i])*positions[i] < ZERO):
               return False
       #print('completed '+str(dest[step]))
       completed = True
       return True
       
    def reset():
        for joint in joints:
            joints[joint].setVelocity(1)
            joints[joint].setPosition(ZERO) 
              
    for name in jointNames:
        #wheels.append(robot.getDevice(name))
        joints[name] = robot.getDevice(name)
        joints[name].getPositionSensor().enable(1)
        
    print(joints['leg_left'])
    
    left_step = True
    VEL = 2
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    prev_key = -1
    
    step = ZERO
    pA = [ZERO, BBB, ZERO, AAA]
    pB = [CCC, BBB, CCC, AAA]
    pBb = [ZERO, BBB, ZERO, AAA]
    pC = [CCC, CCC, CCC, DDD]
    pCb = [ZERO, CCC, ZERO, DDD]
    pD = [AAA, CCC, AAA, DDD]
    pDb = [ZERO, CCC, ZERO, DDD]
    pE = [AAA, BBB, AAA, AAA]
    pEb = [ZERO, BBB, ZERO, AAA]
    pZ = [ZERO, CCC, ZERO, DDD]
    
    step = ZERO
    bA = [ZERO, BBB, ZERO, AAA]
    bB = [AAA, BBB, AAA, AAA]
    #bBb = [ZERO, BBB, ZERO, AAA]
    bC = [AAA, CCC, AAA, DDD]
    #bCb = [ZERO, CCC, ZERO, DDD]
    bD = [CCC, CCC, CCC, DDD]
    #bDb = [ZERO, CCC, ZERO, DDD]
    bE = [CCC, BBB, CCC, AAA]
    #bEb = [ZERO, BBB, ZERO, AAA]
    bZ = [ZERO, CCC, ZERO, DDD]
    #pF = [CCC, BBB, CCC, AAA]
    trA = [ZERO, CCC, ZERO, DDD]
    trB = [ZERO, CCC, TURNB, DDD]
    trC = [ZERO, BBB, TURNB, AAA]
    trD = [ZERO, BBB, ZERO, AAA]
    
    tlA = [ZERO, BBB, ZERO, AAA]
    tlB = [TURNA, BBB, ZERO, AAA]
    tlC = [TURNA, CCC, ZERO, DDD]
    tlD = [ZERO, CCC, ZERO, DDD]
    
    vA = [2, 1, 2, 2]
    vB = [2, 1, 2, 2]
    vC = [2, 2, 2, 1]
    vD = [2, 2, 2, 1]
    vE = [2, 1, 2, 2]
    vF = [2, 1, 2, 2]
    vZ = [2, 2, 2, 1]
    dest = (pA, pB, pC, pD, pE)#, pF)# [CCC, CCC, CCC, DDD])#, [AAA, CCC, AAA, DDD])
    stop = (pA, pBb, pCb, pDb, pEb)
    vel = (vA, vB, vC, vD, vE)#, vF)#, [2, 1, 2, 2])#, [2, 2, 2, 1], [2, 2, 2, 1])
    
    go = True
    resetting = False
    state = '0'
    stopping = False
    turnLeft = False
    turnRight = False
    forward = False
    backward = False
    
    while robot.step(timestep) != -1:
        key=keyboard.getKey()
        completed = False
        prev_state = state
           
        if state=='0':
            reach([ZERO,ZERO,ZERO,ZERO],[1,1,1,1])
            stopping = False
            if turnLeft:
                state='tlA'
            if turnRight:
                state='trA'
            if backward:
                state='bA'
            if forward:
                state='pA'                
        
        if state=='tlA':  
            if reach(tlA,[2,2,2,1]):
                state='tlB'
        if state=='tlB':  
            if reach(tlB,[2,2,2,2]):
                state='tlC'
        if state=='tlC':  
            if reach(tlC,[2,1,2,2]):
                state='tlD'
        if state=='tlD':
            #turnLeft = False  
            if reach(tlD,[2,2,2,2]):
                state='0'  
                
        if state=='trA':  
            if reach(trA,[2,1,2,2]):
                state='trB'
        if state=='trB':  
            if reach(trB,[2,2,2,2]):
                state='trC'
        if state=='trC':  
            if reach(trC,[2,2,2,1]):
                state='trD'
        if state=='trD':
            #turnRight = False  
            if reach(trD,[2,2,2,2]):
                state='0'     
                        
        if state=='pA':
            if reach(pA,vA):
                state='pB'
                if stopping:
                    state = '0' 
        if state=='pZ':
            if reach(pZ,vZ):
                state = '0'
        if state=='pB':
            if reach(pB,vB):
                state='pC'
                if stopping:
                    state='pA'
        if state=='pC':
            if reach(pC,vC):
                state='pD'
                if stopping:
                    state='pZ'
        if state=='pD':
            if reach(pD,vD):
                state='pE'
                if stopping:
                    state='pZ'
        if state=='pE':
            if reach(pE,vE):
                state='pB'
                if stopping:
                    state='pA'
        
        if state=='bA':
            if reach(bA,vA):
                state='bB'
                if stopping:
                    state = '0' 
        if state=='bZ':
            if reach(bZ,vZ):
                state = '0'
        if state=='bB':
            if reach(bB,vB):
                state='bC'
                if stopping:
                    state='bA'
        if state=='bC':
            if reach(bC,vC):
                state='bD'
                if stopping:
                    state='bZ'
        if state=='bD':
            if reach(bD,vD):
                state='bE'
                if stopping:
                    state='bZ'
        if state=='bE':
            if reach(bE,vE):
                state='bB'
                if stopping:
                    state='bA'
        
                
        if key==ord('X'):
            stopping = True
            turnRight = False
            turnLeft = False
            forward = False
            backward = False
            
        if key==ord('A'):
            stopping = True
            turnRight = True
            forward = False
            backward = False
            
        if key==ord('D'):
            stopping = True
            turnLeft = True
            forward = False
            backward = False
            
        if key==ord('S'):
            if not backward:
                stopping = True
            turnRight = False
            turnLeft = False
            forward = False
            backward = True
            
        if key==ord('W'):
            if not forward:
                stopping = True
            turnRight = False
            turnLeft = False
            backward = False
            forward = True
            
        if state != prev_state:
            print(state)
    
x = threading.Thread(target=remote)
x.start() 
#window.mainloop()