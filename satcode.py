import time
from adafruit_crickit import crickit
servos = (crickit.servo_1, crickit.servo_3)

#RIGHT AND LEFT IS DEFINED AS FROM STEVE'S PERSPECTIVE 
#servo 1 is the right - on pin 3
#servo 0 is the left - on pin 1 

#before he sees anything
def steve_sleeping():
    #servos = (crickit.servo_1, crickit.servo_3)
    print ("I see nothing")
    servos[1].angle = 60 
    servos[0].angle = 0
    time.sleep(2)

#once detected a face
def steve_sees_you():
    #servos = (crickit.servo_1, crickit.servo_3)
    print ("about to move arms")
    servos[1].angle = 40 
    servos[0].angle = 20
    time.sleep(0.5)
    
def steve_gives_options():
    #servos = (crickit.servo_1, crickit.servo_3)
    print ("offering options")
    servos[1].angle = 40 
    servos[0].angle = 20
    time.sleep(1)
    servos[1].angle = 10
    time.sleep(0.5) 
    servos[0].angle = 40
    time.sleep(0.2)
    
    
def steve_recieved_your_choice(decision): 
   # servos = (crickit.servo_1, crickit.servo_3)
    if decision == "right":
        print ("steve's right option was chosen")
        print("i'm moving my right hand")
        servos[1].angle = 0
        servos[0].angle = 0
        time.sleep(1)
    elif decision == "left":
        print ("steve's left option was chosen")
        print("i'm moving my left hand")
        servos[1].angle = 60
        servos[0].angle = 60
        time.sleep(1)
    else: 
        servos[1].angle = 10
        servos[0].angle = 25
        time.sleep(0.8)
        servos[1].angle = 15
        servos[0].angle = 20
        time.sleep(1)
        
   
def main():    
    #servos = (crickit.servo_1, crickit.servo_3)
    choice = "left"
    steve_sleeping()
    #steve_sees_you()
    #steve_gives_options()
    #steve_recieved_your_choice(choice)
    
    #TODO put the other functions in 
    
if __name__ == '__main__':
        main() 
    
