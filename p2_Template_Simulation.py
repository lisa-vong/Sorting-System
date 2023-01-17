## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
sys.path.append('../')

from Common_Libraries.p2_sim_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()
update_thread = repeating_timer(2, update_sim)

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
import random
arm.home()

def get_dropoff (container_id): #retrieves drop off location corresponding to container id
    if container_id == 1: #small, red
        drop_off = [-0.589, 0.238, 0.452] #top of red autoclave
    elif container_id == 2:#small, green
        drop_off = [0.0, -0.643, 0.42] #top of green autoclave
    elif container_id == 3: #small, blue
        drop_off = [0.0, 0.643, 0.42] #top of blue autoclave
    elif container_id == 4: #big, red
        drop_off = [-0.385, 0.164, 0.297] #red autoclave drawer
    elif container_id == 5: #big, green
        drop_off = [0.0, -0.42, 0.273] #green autoclave drawer
    elif container_id == 6: #big, blue
        drop_off = [0.0, 0.42, 0.273] #blue autoclave drawer
        
    return drop_off

def control_gripper(gripper_open):
    while arm.emg_left()>0.2  and arm.emg_right()<0.2: #Only left above threshold // controls gripper
        if gripper_open == True: #True indicates gripper is open //closes gripper if the gripper is currently open
            arm.control_gripper(32)
            time.sleep(4)
        else: #False indicates gripper is closed // opens the gripper if the gripper is currently closed
            arm.control_gripper(-32)
            time.sleep(4)

def move_end_effector (gripper_open, container_id):
    while arm.emg_left()<0.2  and arm.emg_right()>0.2: #Only right above threshold // move end effector
        if gripper_open == True: #moves to pickup position if the gripper is open
            arm.move_arm(0.532, 0.0, 0.035) #pick up location
            time.sleep(4)
        else: #moves to drop off location if the gripper is closed
            drop_off = get_dropoff(container_id)
            arm.move_arm(0.406,0.0,0.483) #home position
            time.sleep(2)
            arm.move_arm(drop_off[0],drop_off[1],drop_off[2]) #drop off location
            time.sleep(4)

def autoclave_drawer (autoclave_open, container_id):
    while arm.emg_left()>0.2  and arm.emg_right()>0.2: #Both above threshold // opens or closes autoclave bin drawer
        if autoclave_open == True: #True indicates that drawer is open // Closes drawer if drawer is currently open
            if container_id == 4: #big, red
                arm.open_red_autoclave(False) 
            elif container_id == 5: #big, green
                arm.open_green_autoclave(False) 
            elif container_id == 6: #big, blue
                arm.open_blue_autoclave(False) 
            time.sleep(4)
        else: #False indicates that drawer is closed // Opens drawer if drawer is currently closed
            if container_id == 4: #big, red
                arm.open_red_autoclave(True)
            elif container_id == 5: #big, green
                arm.open_green_autoclave(True)
            elif container_id == 6: #big, blue
                arm.open_blue_autoclave(True) 
            time.sleep(4)
    
def sleep():
    while arm.emg_left()<=0.2  and arm.emg_right()<=0.2: #if both are below threshold // Q arm is stationary
        time.sleep(1)

def main ():
    container_id_list = [1, 2, 3, 4, 5, 6] #list of container IDs
    random.shuffle(container_id_list) #randomizes list of IDs 
    for i in container_id_list: #loops through process 6 times
        container_id = int(i) #sets ID to a variable as integer value 
        arm.spawn_cage(container_id) #spawns container corresponding to the ID
        arm.home() #sets Q arm to home position
        sleep()
        move_end_effector (True, container_id) #moves to pick up location
        sleep()
        control_gripper(True) #closes gripper
        if i > 3: #goes through autoclave drawer opening process if ID is greater than 3 (big containers)
            sleep()
            autoclave_drawer(False, container_id) #opens drawer
            sleep()
        move_end_effector (False, container_id) #moves to drop off location
        sleep()
        control_gripper(False) #opens gripper
        if i > 3: #goes through autoclave drawer closing process if ID is greater than 3 (big containers)
            sleep()
            autoclave_drawer(True, container_id) #closes drawer
        arm.home() #returns to home position
        time.sleep(4)
    arm.home() #brings back to home position after all containers are placed
    print ("All containers have been successfully placed")
    arm.terminate_arm() #terminates arm

main()
  
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#--------------------------------------------------------------------------------
