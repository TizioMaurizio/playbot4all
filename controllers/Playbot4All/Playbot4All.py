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
    wheels = []
    jointNames = ['hip_right','leg_right','hip_left','leg_left']
    positionLimits = { 'leg_left': [0.6,-0.3], 'leg_right': [0.3,-0.6], 'hip_left': [0.6, -0.6], 'hip_right': [0.6, -0.6] }
    tolerance = 0.01
    joints = dict()
    
    def pos(joint):
        return joints[joint].getPositionSensor().getValue()

    def moving(joint, n):
        if(pos(joint)*positionLimits[joint][n]) < 0:
            return True
        else:
            return abs(pos(joint)) < abs(positionLimits[joint][n]) - tolerance
    
    def hip_left(dir):
        if(dir):
            joints['hip_left'].setPosition(positionLimits['hip_left'][0])
            joints['hip_left'].setVelocity(velocity)
        else:
            joints['hip_left'].setPosition(positionLimits['hip_left'][1])
            joints['hip_left'].setVelocity(velocity)
            
    def hip_right(dir):
        if(dir):
            joints['hip_right'].setPosition(positionLimits['hip_right'][0])
            joints['hip_right'].setVelocity(velocity)
        else:
            joints['hip_right'].setPosition(positionLimits['hip_right'][1])
            joints['hip_right'].setVelocity(velocity)
    
    def leg_left(dir):
        if(dir):
            joints['leg_left'].setPosition(positionLimits['leg_left'][0])
            joints['leg_left'].setVelocity(velocity)
        else:
            joints['leg_left'].setPosition(positionLimits['leg_left'][1])
            joints['leg_left'].setVelocity(velocity)
            
    def leg_right(dir):
        if(dir):
            joints['leg_right'].setPosition(positionLimits['leg_right'][0])
            joints['leg_right'].setVelocity(velocity)
        else:
            joints['leg_right'].setPosition(positionLimits['leg_right'][1])
            joints['leg_right'].setVelocity(velocity)
    
    def lean_left(dir):
        leg_left(not dir)
        leg_right(not dir)      
       
    def forward(dir):
        hip_left(dir)
        hip_right(dir)      
    
    completed = False
    def goto(positions,velocities):
       velocity = 1
       joints['hip_right'].setPosition(positions[0])
       joints['hip_right'].setVelocity(velocities[0])
       joints['leg_right'].setPosition(positions[1])
       joints['leg_right'].setVelocity(velocities[1])
       joints['hip_left'].setPosition(positions[2])
       joints['hip_left'].setVelocity(velocities[2])
       joints['leg_left'].setPosition(positions[3])
       joints['leg_left'].setVelocity(velocities[3])
                   
    
    def complete(positions):
       for i in range(4):
           if(abs(abs(pos(jointNames[i])) - abs(positions[i])) > tolerance or pos(jointNames[i])*positions[i] < 0):
               return False
       print('completed '+str(dest[step]))
       completed = True
       return True
               
    for name in jointNames:
        #wheels.append(robot.getDevice(name))
        joints[name] = robot.getDevice(name)
        joints[name].getPositionSensor().enable(1)
        
    print(joints['leg_left'])
    
    left_step = True
    VEL = 4
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    prev_key = -1
    
        
    while robot.step(timestep) != -1:#
        
        key=keyboard.getKey()
        if key != prev_key:
            print(key)
            if key==-1:
                velocity = 0
                for joint in joints:
                    try:
                        joints[joint].setVelocity(velocity)
                    except:
                        print('error stopping motor', joint)
                        
            velocity = VEL
            if key==ord('D'): #forward
                if(left_step):
                    if(moving('leg_left', 1)):
                        print('leg_left '+str(pos('leg_left')))
                        #key=ord('T')
                        lean_left(left_step)
                    else:
                        if(moving('hip_left', 0)):
                            print('hip_left '+str(pos('hip_left')))
                            #key=ord('F')
                            forward(left_step)
                        else:
                            left_step = False
                            print(left_step)
                else:
                    if(moving('leg_right', 0)):
                        print('leg_right '+str(pos('leg_right')))
                        #key=ord('R')
                        lean_left(left_step)
                    else:
                        if(moving('hip_right', 1)):
                            print('hip_right '+str(pos('hip_right')))
                            #key=ord('G')
                            forward(left_step)
                        else:
                            print('end')
                            left_step = True
                key = -2
                    
            if key==ord('C'): #backward
                if(left_step):
                    if(moving('leg_left', 1)):
                        print('leg_left '+str(pos('leg_left')))
                        #key=ord('T')
                        lean_left(left_step)
                    else:
                        if(moving('hip_left', 1)):
                            print('hip_left '+str(pos('hip_left')))
                            #key=ord('F')
                            forward(not left_step)
                        else:
                            left_step = False
                            print(left_step)
                else:
                    if(moving('leg_right', 0)):
                        print('leg_right '+str(pos('leg_right')))
                        #key=ord('R')
                        lean_left(left_step)
                    else:
                        if(moving('hip_right', 0)):
                            print('hip_right '+str(pos('hip_right')))
                            #key=ord('G')
                            forward(not left_step)
                        else:
                            print('end')
                            left_step = True
                key = -2
                
            if key==ord('X'): #stopleg
                if(moving('leg_left', 1) or moving('leg_right', 0)):
                    joints['leg_right'].setPosition(0)
                    joints['leg_right'].setVelocity(velocity)
                    joints['leg_left'].setPosition(0)
                    joints['leg_left'].setVelocity(velocity)
                    left_step = True
                    
            if key==ord('Z'): #stophip
                if(moving('hip_left', 1) or moving('hip_right', 1)):
                    joints['hip_right'].setPosition(0)
                    joints['hip_right'].setVelocity(velocity)
                    joints['hip_left'].setPosition(0)
                    joints['hip_left'].setVelocity(velocity)
                    left_step = True
                              
            if key==ord('V'): #turn left
                if(left_step):
                    if(moving('leg_left', 1)):
                        print('leg_left '+str(pos('leg_left')))
                        #key=ord('T')
                        lean_left(left_step)
                    else:
                        if(moving('hip_left', 0)):
                            print('hip_left '+str(pos('hip_left')))
                            #key=ord('F')
                            hip_left(left_step)
                        else:
                            left_step = False
                            print(left_step)
                else:
                    if(abs(pos('leg_right')) > tolerance):
                        print('leg_right '+str(pos('leg_right')))
                        #key=ord('R')
                        joints['leg_right'].setPosition(0)
                        joints['leg_right'].setVelocity(velocity)
                        joints['leg_left'].setPosition(0)
                        joints['leg_left'].setVelocity(velocity)
                    else:
                        if(moving('leg_right', 1)):
                            lean_left(left_step)
                        else:
                            joints['hip_right'].setPosition(0)
                            joints['hip_right'].setVelocity(velocity)
                            joints['hip_left'].setPosition(0)
                            joints['hip_left'].setVelocity(velocity)
                key = -2
                       
            #if key==ord('X'): #left
                #key=ord('Q')
            if key==ord('V'): #right
                key=ord('A')
                
            if key==ord('R'):
                key=ord('W')
            if key==ord('T'):
                key=ord('S')
            if key==ord('F'):
                key=ord('Q')
            if key==ord('G'):
                key=ord('A')
                
            if key==ord('Q'):
                joints['hip_left'].setPosition(positionLimits['hip_left'][0])
                joints['hip_left'].setVelocity(velocity)
                key=ord('L')
            if key==ord('W'):
                joints['leg_left'].setPosition(positionLimits['leg_left'][0])
                joints['leg_left'].setVelocity(velocity)
                key=ord('I')
            if key==ord('A'):
                joints['hip_left'].setPosition(positionLimits['hip_left'][1])
                joints['hip_left'].setVelocity(velocity)
                key=ord('O')
            if key==ord('S'):
                joints['leg_left'].setPosition(positionLimits['leg_left'][1])
                joints['leg_left'].setVelocity(velocity/2)
                key=ord('K')
            if key==ord('L'):
                joints['hip_right'].setPosition(positionLimits['hip_right'][0])
                joints['hip_right'].setVelocity(velocity)
            if key==ord('K'):
                joints['leg_right'].setPosition(positionLimits['leg_right'][1])
                joints['leg_right'].setVelocity(velocity)
            if key==ord('O'):
                joints['hip_right'].setPosition(positionLimits['hip_right'][1])
                joints['hip_right'].setVelocity(velocity)
            if key==ord('I'):
                joints['leg_right'].setPosition(positionLimits['leg_right'][0])
                joints['leg_right'].setVelocity(velocity/2)
            #if key==ord('Z'):
            if key==-9:
                for joint in joints:
                    joints[joint].setVelocity(velocity/4)
                    joints[joint].setPosition(0)
        # Read the sensors:
        # Enter here functions to read sensor data, like:
        #  val = ds.getValue()
    
        # Process sensor data here.
    
        # Enter here functions to send actuator commands, like:
        #  motor.setPosition(10.0)
        prev_key = key
    
    # Enter here exit cleanup code.
    
        
x = threading.Thread(target=remote)
x.start() 
#window.mainloop()