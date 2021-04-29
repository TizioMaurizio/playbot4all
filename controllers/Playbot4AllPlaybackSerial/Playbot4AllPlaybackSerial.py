"""4wheelController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Keyboard
from controller import Motor, Brake, PositionSensor
import tkinter as tk
import threading
import time
import serial
import json
import jsonhandler

RATE = 0.1
# create the Robot instance.
robot = Robot()
window = tk.Tk()
greeting = tk.Label(text="Hello, Webots")
greeting.pack()


#x = threading.Thread(target=serialRead)
#x.start() 


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
   
    AAA = 0.4
    BBB = 0.15
    CCC = -0.4
    DDD = -0.15
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
    pAdeg = [int(ZERO*57.29+90), int(BBB*57.29+90), int(ZERO*57.29+90), int(AAA*57.29+90)]
    #pAdeg = [int(180), int(180), int(180), int(180)]
    pB = [CCC, BBB, CCC, AAA]
    pBdeg = [int(CCC*57.29+90), int(BBB*57.29+90), int(CCC*57.29+90), int(AAA*57.29+90)]
    #pBdeg = [int(180), int(180), int(180), int(180)]
    pBb = [ZERO, BBB, ZERO, AAA]
    pC = [CCC, CCC, CCC, DDD]
    pCdeg = [int(CCC*57.29+90), int(CCC*57.29+90), int(CCC*57.29+90), int(DDD*57.29+90)]
    pCb = [ZERO, CCC, ZERO, DDD]
    pD = [AAA, CCC, AAA, DDD]
    pDdeg = [int(AAA*57.29+90), int(CCC*57.29+90), int(AAA*57.29+90), int(DDD*57.29+90)]
    pDb = [ZERO, CCC, ZERO, DDD]
    pE = [AAA, BBB, AAA, AAA]
    pEdeg = [int(AAA*57.29+90), int(BBB*57.29+90), int(AAA*57.29+90), int(AAA*57.29+90)]
    pEb = [ZERO, BBB, ZERO, AAA]
    pZ = [ZERO, CCC, ZERO, DDD]
    pZdeg = [int(ZERO*57.29+90), int(CCC*57.29+90), int(ZERO*57.29+90), int(DDD*57.29+90)]
    
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
    
    """
    receiving = False
    jsonready = False
    recjson = ''
    par = 0
    """
    
    prevtime = 0
    
    while robot.step(timestep) != -1:
        jsonhandler.loop()
        """  
        x = ard.read()
        if x == b'{':
            par+=1
            recjson+=x.decode("utf8")
            receiving = True
        
        if receiving:
            recjson+=x.decode("utf8")
            if x == b'}':
                par-=1
                recjson+=x.decode("utf8")
                if(par == 0):
                    receiving = False
                    jsonready = True
                
        if jsonready:
            jsonready = False
            print ('Message from arduino: ')
            print (recjson)
            recjson = ''
        """
        
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
            if state != prev_state:
                jsonhandler.send({"servo":pAdeg,"next":pBdeg})
            try:
                if(jsonhandler.getPlaybot()["servo"]==pAdeg or jsonhandler.getPlaybot()["servo"]==jsonhandler.getPlaybot()["next"]):
                    if reach(pA,vA):
                        pass
                    if(jsonhandler.getPlaybot()["ready"] or jsonhandler.getPlaybot()["servo"]==jsonhandler.getPlaybot()["next"]):
                        if stopping:
                            state = '0'
                        else: 
                            state='pB'
            except:
                pass
                
        if state=='pZ':
            if state != prev_state:
                jsonhandler.send({"servo":pZdeg})
            try:
                if(jsonhandler.getPlaybot()["servo"]==pZdeg):
                    if reach(pZ,vZ):
                        pass
                    if(jsonhandler.getPlaybot()["ready"]):
                        state = '0'
            except:
                pass
                
        if state=='pB':
            if state != prev_state:
                jsonhandler.send({"servo":pBdeg})
            try:
                if(jsonhandler.getPlaybot()["servo"]==pBdeg):
                    if reach(pB,vB):
                        pass
                    if(jsonhandler.getPlaybot()["ready"]):
                        if stopping:
                            state='pA'
                        else:
                            state='pC'
                else:
                    jsonhandler.send({"servo":pBdeg})
            except:
                pass
                
        if state=='pC':
            if state != prev_state:
                jsonhandler.send({"servo":pCdeg})
            try:
                if(jsonhandler.getPlaybot()["servo"]==pCdeg):
                    if reach(pC,vC):
                        pass
                    if(jsonhandler.getPlaybot()["ready"]):
                        if stopping:
                            state='pZ'
                        else:
                            state='pD'
            except:
                pass
                        
        if state=='pD':
            if state != prev_state:
                jsonhandler.send({"servo":pDdeg})
            try:
                if(jsonhandler.getPlaybot()["servo"]==pDdeg):
                    if reach(pD,vD):
                        pass
                    if(jsonhandler.getPlaybot()["ready"]):
                        if stopping:
                            state='pZ'
                        else:
                            state='pE'
            except:
                pass
                               
        if state=='pE':
            if state != prev_state:
                jsonhandler.send({"servo":pEdeg})
            try:
                if(jsonhandler.getPlaybot()["servo"]==pEdeg):
                    if reach(pE,vE):
                        pass
                    if(jsonhandler.getPlaybot()["ready"]):
                        if stopping:
                            state='pA'
                        else:
                            state='pB'
            except:
                pass
                
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
            
        if key==ord('Q'): 
            ard.write(b'{"servo":{"hip_right":0,"leg_right":0,"hip_left":0,"leg_left":0}}')
            
        if state != prev_state:
            print(state)
    
x = threading.Thread(target=remote)
x.start() 
#window.mainloop()