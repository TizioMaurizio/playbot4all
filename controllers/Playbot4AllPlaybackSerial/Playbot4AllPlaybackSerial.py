"""4wheelController controller."""
#REQUIREMENT TO RUN: arduino connected to serial with 
#aaPlaybotArduino running on it, otherwise states will not advance

#GENERAL LOGIC:
#The python states machine sends current and next state to arduino,
#arduino upon completing current state updates the current state using the next state
#doing so the python state machine notices arduino has advanced and sends the next pair of states.
#the case of interruptions is not currently completely managed
#the simulated robot moves at a different speed from the real one, so it is possible that it skids or skips steps
#
#this robot is a REFLECTION of the actual implemented robot on arduino
#if arduino moves too fast the simulation can't keep up and the robot
#skids and turns

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Keyboard
from controller import Motor, Brake, PositionSensor
import time
import serial
import json
import jsonhandler

RATE = 0.1
# create the Robot instance.
robot = Robot()

state = '0'
prev_state = '0'

def remote():
    global state, prev_state
    #SET UP THE ROBOT
    timestep = int(robot.getBasicTimeStep())
    
    #START KEYBOARD DETECTION
    keyboard=Keyboard()
    keyboard.enable(timestep)
    
    #ROBOT GAIT PARAMETERS
    #each of these variables defines the target angles for the gait
    #0.4, 0.15 tall robot, 0.4,0.3 short robot
    #THURST AND MAXIMUM LEAN ARE COUPLED, MINIMUM LEAN AND TURN ARE DECOUPLED
    AAA = 0.4 #left push and forward
    BBB = 0.25*1 #left lean
    CCC = -0.4 #right push and forward
    DDD = -0.25*1 #right lean
    TURNA = -0.3 #left turn
    TURNB = 0.3 #right turn
    ZERO = 0

    
    #SET UP THE ROBOT
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
               #joints['hip_right'].setVelocity(velocities[ZERO])
               joints['leg_right'].setPosition(positions[1])
               #joints['leg_right'].setVelocity(velocities[1])
               joints['hip_left'].setPosition(positions[2])
               #joints['hip_left'].setVelocity(velocities[2])
               joints['leg_left'].setPosition(positions[3])
               #joints['leg_left'].setVelocity(velocities[3])
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

    left_step = True
    VEL = 6
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    prev_key = -1
    #END SET UP THE ROBOT
    
    #SET UP THE FINITE-STATE AUTOMATON
    def stateToDeg(array):
        array = [round(array[0]*57.29+90), round(array[1]*57.29+90), round(array[2]*57.29+90), round(array[3]*57.29+90)]
        return array    
            
    step = ZERO
    pA = [ZERO, BBB, ZERO, AAA]
    pAdeg = stateToDeg(pA)
    #pAdeg = [int(180), int(180), int(180), int(180)]
    pB = [CCC, BBB, CCC, AAA]
    pBdeg = stateToDeg(pB)
    #pBdeg = [int(180), int(180), int(180), int(180)]
    pBb = [ZERO, BBB, ZERO, AAA]
    pC = [CCC, CCC, CCC, DDD]
    pCdeg = stateToDeg(pC)
    pCb = [ZERO, CCC, ZERO, DDD]
    pD = [AAA, CCC, AAA, DDD]
    pDdeg = stateToDeg(pD)
    pDb = [ZERO, CCC, ZERO, DDD]
    pE = [AAA, BBB, AAA, AAA]
    pEdeg = stateToDeg(pE)
    pEb = [ZERO, BBB, ZERO, AAA]
    pZ = [ZERO, CCC, ZERO, DDD]
    pZdeg = stateToDeg(pZ)
    
    ZEROdeg = [ZERO+90,ZERO+90,ZERO+90,ZERO+90]
    
    step = ZERO
    bA = [ZERO, BBB, ZERO, AAA]
    bAdeg = stateToDeg(bA)
    bB = [AAA, BBB, AAA, AAA]
    bBdeg = stateToDeg(bB)
    #bBb = [ZERO, BBB, ZERO, AAA]
    bC = [AAA, CCC, AAA, DDD]
    bCdeg = stateToDeg(bC)
    #bCb = [ZERO, CCC, ZERO, DDD]
    bD = [CCC, CCC, CCC, DDD]
    bDdeg = stateToDeg(bD)
    #bDb = [ZERO, CCC, ZERO, DDD]
    bE = [CCC, BBB, CCC, AAA]
    bEdeg = stateToDeg(bE)
    #bEb = [ZERO, BBB, ZERO, AAA]
    bZ = [ZERO, CCC, ZERO, DDD]
    bZdeg = stateToDeg(bZ)
    #pF = [CCC, BBB, CCC, AAA]
    trA = [ZERO, CCC, ZERO, DDD]
    trAdeg = stateToDeg(trA)
    trB = [ZERO, CCC, TURNB, DDD]
    trBdeg = stateToDeg(trB)
    trC = [ZERO, BBB, TURNB, AAA]
    trCdeg = stateToDeg(trC)
    trD = [ZERO, BBB, ZERO, AAA]
    trDdeg = stateToDeg(trD)
      
    s = 1 
              
    vrA = [2*s,1*s,2*s,2*s]
    vrB = [2*s,2*s,2*s,2*s]
    vrC = [2*s,2*s,2*s,1*s]
    vrD = [2*s,2*s,2*s,2*s] 
          
    tlA = [ZERO, -DDD, ZERO, -CCC]
    tlAdeg = stateToDeg(tlA)
    tlB = [TURNA, -DDD, ZERO, -CCC]
    tlBdeg = stateToDeg(tlB)
    tlC = [TURNA, -AAA, ZERO, -BBB]
    tlCdeg = stateToDeg(tlC)
    tlD = [ZERO, -AAA, ZERO, -BBB]
    tlDdeg = stateToDeg(tlD)
    
    vlA = [2*s,2*s,2*s,1*s]
    vlB = [2*s,2*s,2*s,2*s]
    vlC = [2*s,1*s,2*s,2*s]
    vlD = [2*s,2*s,2*s,2*s]
    
    vlA = [2*s,2*s,2*s,2*s]
    vlB = [2*s,2*s,2*s,2*s]
    vlC = [2*s,2*s,2*s,2*s]
    vlD = [2*s,2*s,2*s,2*s]
        
    vA = [2*s, 2*s, 2*s, 2*s]
    vB = [2*s, 1*s, 2*s, 2*s]
    vC = [2*s, 2*s, 2*s, 1*s]
    vD = [2*s, 2*s, 2*s, 1*s]
    vE = [2*s, 1*s, 2*s, 2*s]
    vF = [2*s, 1*s, 2*s, 2*s]
    vZ = [2*s, 2*s, 2*s, 1*s]
    
    vA = [2*s, 2*s, 2*s, 2*s]
    vB = [2*s, 2*s, 2*s, 2*s]
    vC = [2*s, 2*s, 2*s, 2*s]
    vD = [2*s, 2*s, 2*s, 2*s]
    vE = [2*s, 2*s, 2*s, 2*s]
    vF = [2*s, 2*s, 2*s, 2*s]
    vZ = [2*s, 2*s, 2*s, 2*s]
    
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
    
    
    def doState(currDeg, nextDeg, curr, currvel, nextName, stopName):
        global state, prev_state
        if state != prev_state:
            jsonhandler.send({"servo":currDeg,"next":nextDeg})
        try:
            if(jsonhandler.getPlaybot()["servo"]==currDeg): #Arduino is reaching the current state
                if reach(curr,currvel):
                    pass
                if stopping:
                    reach(stopName,currvel)
            elif(jsonhandler.getPlaybot()["servo"]==nextDeg): #Arduino completed the current state
                    if stopping:
                        state = stopName
                    else: 
                        state=nextName
            if(jsonhandler.getPlaybot()["next"]!=nextDeg): #Arduino next state not updated
                jsonhandler.send({"servo":currDeg,"next":nextDeg})
                reach(curr,currvel)
        except:
            pass 
            
    def turnState(currDeg, nextDeg, curr, currvel, nextName, stopName):
        global state, prev_state
        if state != prev_state:
            jsonhandler.send({"servo":currDeg,"next":nextDeg})
        try:
            if(jsonhandler.getPlaybot()["servo"]==currDeg): #Arduino is reaching the current state
                if reach(curr,currvel):
                    pass
            elif(jsonhandler.getPlaybot()["servo"]==nextDeg): #Arduino completed the current state
                    state=nextName
            if(jsonhandler.getPlaybot()["next"]!=nextDeg): #Arduino next state not updated
                jsonhandler.send({"servo":currDeg,"next":nextDeg})
        except:
            pass  
    #END SET UP THE FINITE-STATE AUTOMATON
    
    while robot.step(timestep) != -1:
        #USB RECEIVER AND SENDER
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
        
        #READ KEYBOARD
        key=keyboard.getKey()
        
        completed = False
        prev_state = state
        
        #IR SENSOR STOP SIMULATION GIMMICK
        try:
            for i in range(3):
                if jsonhandler.getPlaybot()["irsensor"][i]:# and False:
                    state = '0'
                    stopping = True
                    turnRight = False
                    turnLeft = False
                    forward = False
                    backward = False
        except:
            pass
        
        #BEGIN STATES 
        
        #INITIAL STATE   
        if state=='0':
            turnState(ZEROdeg, ZEROdeg, [ZERO,ZERO,ZERO,ZERO], [1,1,1,1], '0', '0')
            try:
                if(jsonhandler.getPlaybot()["servo"] != ZEROdeg):
                    jsonhandler.send({"servo":ZEROdeg,"next":ZEROdeg})
            except:
                pass
            #reach([ZERO,ZERO,ZERO,ZERO],[1,1,1,1])
            stopping = False
            if turnLeft:
                state='tlA'
            if turnRight:
                state='trA'
            if backward:
                state='bA'
            if forward:
                state='pA'                
        """
        #OLD STATES BEFORE FUNCTIONS
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
            doState(trAdeg, trBdeg, trA, [2,1,2,2], 'trB', 'trB')
            #if reach(trA,[2,1,2,2]):
                #state='trB'
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
        """   
        #TURN LEFT STATES
        if state=='tlA':  
            doState(tlAdeg, tlBdeg, tlA, vlA, 'tlB', 'tlB')
        if state=='tlB':
            doState(tlBdeg, tlCdeg, tlB, vlB, 'tlC', 'tlC')  
        if state=='tlC': 
            doState(tlCdeg, tlDdeg, tlC, vlC, 'tlD', 'tlD') 
        if state=='tlD':
            doState(tlDdeg, ZEROdeg, tlD, vlD, '0', '0')
        
        #TURN RIGHT STATES
        if state=='trA':  
            doState(trAdeg, trBdeg, trA, vrA, 'trB', 'trB')
            #if reach(trA,[2,1,2,2]):
                #state='trB'
        if state=='trB':
            doState(trBdeg, trCdeg, trB, vrB, 'trC', 'trC')  
        if state=='trC': 
            doState(trCdeg, trDdeg, trC, vrC, 'trD', 'trD') 
        if state=='trD':
            doState(trDdeg, ZEROdeg, trD, vrD, '0', '0') 
             
        """        
        #OLD STATES BEFORE FUNCTIONS
                
        if state=='pA':
            if state != prev_state:
                jsonhandler.send({"servo":pAdeg,"next":pBdeg})
            try:
                if(jsonhandler.getPlaybot()["servo"]==pAdeg):
                    if reach(pA,vA):
                        pass
                    if stopping:
                        state = '0'
                elif(jsonhandler.getPlaybot()["servo"]==pBdeg):
                        if stopping:
                            state = '0'
                        else: 
                            state='pB'
                if(jsonhandler.getPlaybot()["next"]!=pBdeg):
                    jsonhandler.send({"servo":pAdeg,"next":pBdeg})
            except:
                pass
        """
        
        #GO FORWARD STATES
        if state=='pA':
            doState(pAdeg, pBdeg, pA, vA, 'pB', '0')
                
        if state=='pZ':
            doState(pZdeg, ZEROdeg, pZ, vZ, '0', '0')  
                  
        if state=='pB':
            doState(pBdeg, pCdeg, pB, vB, 'pC', 'pA')
                
        if state=='pC':
            doState(pCdeg, pDdeg, pC, vC, 'pD', 'pZ')
                        
        if state=='pD':
            doState(pDdeg, pEdeg, pD, vD, 'pE', 'pZ')
                               
        if state=='pE':
            doState(pEdeg, pBdeg, pE, vE, 'pB', 'pA')
            
        """
        #OLD STATES BEFORE FUNCTIONS
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
        """
        """        
        #OLD STATES BEFORE FUNCTIONS
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
        """
        
        #GO BACKWARD STATES
        if state=='bA':
            doState(bAdeg, bBdeg, bA, vA, 'bB', '0')
            
        if state=='bZ':
            doState(bZdeg, ZEROdeg, bZ, vZ, '0', '0')
            
        if state=='bB':
            doState(bBdeg, bCdeg, bB, vB, 'bC', 'bA')
            
        if state=='bC':
            doState(bCdeg, bDdeg, bC, vC, 'bD', 'bZ')
            
        if state=='bD':
            doState(bDdeg, bEdeg, bD, vD, 'bE', 'bZ')
            
        if state=='bE':
            doState(bEdeg, bBdeg, bE, vE, 'bB', 'bA')
        
        if state != prev_state:
            print(state)
             
        #READ INPUT        
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
            turnLeft = False
            
        if key==ord('D'):
            stopping = True
            turnLeft = True
            forward = False
            backward = False
            turnRight = False
            
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
        

#START THE CONTROLLER
remote()