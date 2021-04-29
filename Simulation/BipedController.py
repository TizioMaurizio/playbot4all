"""4wheelController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Keyboard
import tkinter as tk
import threading
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
    jointNames = ['hip_right','leg_right','knee_right','ankle_right','foot_right','hip_left','leg_left','knee_left','ankle_left','foot_left']
    joints = dict()
    for name in jointNames:
        #wheels.append(robot.getDevice(name))
        joints[name] = robot.getDevice(name)
        
    print(joints['leg_left'])
    VEL = 1
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    prev_key = -1
    while robot.step(timestep) != -1:
        key=keyboard.getKey()
        print(key)
        if key != prev_key:
            if key==-1:
                velocity = 0
                for joint in joints:
                    try:
                        joints[joint].setVelocity(velocity)
                    except:
                        print('error stopping motor', joint)
            if key==ord('Q'):
                velocity = VEL
                joints['hip_left'].setPosition(float('inf'))
                joints['hip_left'].setVelocity(velocity)
            if key==ord('W'):
                velocity = VEL
                joints['leg_left'].setPosition(float('inf'))
                joints['leg_left'].setVelocity(velocity)
            if key==ord('E'):
                velocity = VEL
                joints['knee_left'].setPosition(float('inf'))
                joints['knee_left'].setVelocity(velocity)
            if key==ord('R'):
                velocity = VEL
                joints['ankle_left'].setPosition(float('inf'))
                joints['ankle_left'].setVelocity(velocity)
            if key==ord('T'):
                velocity = VEL
                joints['foot_left'].setPosition(float('inf'))
                joints['foot_left'].setVelocity(velocity)
            if key==ord('A'):
                velocity = -VEL
                joints['hip_left'].setPosition(float('inf'))
                joints['hip_left'].setVelocity(velocity)
            if key==ord('S'):
                velocity = -VEL
                joints['leg_left'].setPosition(float('inf'))
                joints['leg_left'].setVelocity(velocity)
            if key==ord('D'):
                velocity = -VEL
                joints['knee_left'].setPosition(float('inf'))
                joints['knee_left'].setVelocity(velocity)
            if key==ord('F'):
                velocity = -VEL
                joints['ankle_left'].setPosition(float('inf'))
                joints['ankle_left'].setVelocity(velocity)
            if key==ord('G'):
                velocity = -VEL
                joints['foot_left'].setPosition(float('inf'))
                joints['foot_left'].setVelocity(velocity)
            if key==ord('P'):
                velocity = VEL
                joints['hip_right'].setPosition(float('inf'))
                joints['hip_right'].setVelocity(velocity)
            if key==ord('O'):
                velocity = VEL
                joints['leg_right'].setPosition(float('inf'))
                joints['leg_right'].setVelocity(velocity)
            if key==ord('I'):
                velocity = VEL
                joints['knee_right'].setPosition(float('inf'))
                joints['knee_right'].setVelocity(velocity)
            if key==ord('U'):
                velocity = VEL
                joints['ankle_right'].setPosition(float('inf'))
                joints['ankle_right'].setVelocity(velocity)
            if key==ord('Y'):
                velocity = VEL
                joints['foot_right'].setPosition(float('inf'))
                joints['foot_right'].setVelocity(velocity)
            if key==210:
                velocity = -VEL
                joints['hip_right'].setPosition(float('inf'))
                joints['hip_right'].setVelocity(velocity)
            if key==ord('L'):
                velocity = -VEL
                joints['leg_right'].setPosition(float('inf'))
                joints['leg_right'].setVelocity(velocity)
            if key==ord('K'):
                velocity = -VEL
                joints['knee_right'].setPosition(float('inf'))
                joints['knee_right'].setVelocity(velocity)
            if key==ord('J'):
                velocity = -VEL
                joints['ankle_right'].setPosition(float('inf'))
                joints['ankle_right'].setVelocity(velocity)
            if key==ord('H'):
                velocity = -VEL
                joints['foot_right'].setPosition(float('inf'))
                joints['foot_right'].setVelocity(velocity)
            if key==ord('Z'):
                velocity = VEL
                wheels[4].setPosition(0)
                wheels[4].setVelocity(velocity)
                wheels[5].setPosition(-1.1)
                wheels[5].setVelocity(velocity)
                wheels[6].setPosition(1.5)
                wheels[6].setVelocity(velocity)
                wheels[7].setPosition(0)
                wheels[7].setVelocity(velocity)
                wheels[8].setPosition(0)
                wheels[8].setVelocity(velocity)
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