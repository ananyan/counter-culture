#import standard libraries and packages
import picamera
import pygame as pg 
import os 

from google.cloud import vision
import time 
from time import sleep 
from adafruit_crickit import crickit 
import signal 
import sys 
import re

import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../DET190-JSON/Pinky-DET-2019-e4f4274adb35.json"
client = vision.ImageAnnotatorClient()

image = 'image.jpeg'

# take in an image
def take_photo(camera):
    camera.start_preview()
    sleep(0.5)
    camera.capture('image.jpeg')
    camera.stop_preview()

# figure out where the person/object is in the image
def localize_objects(image):
    """Localize objects in the local image.
    
    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()
    
    objects = client.object_localization(image=image).localized_object_annotations
     
    for object_ in objects: #the _ normally means run it but don't grab it
        #print('\n{} (confidence: {})'.format(object_.name, object_.score))
        area = 0
        if object_.name == 'Person':
            vertices = object_.bounding_poly.normalized_vertices
            #print(vertices) #counterclockwise from bottom left
            length = abs(vertices[0].x - vertices[1].x)
            height = abs(vertices[1].y - vertices[2].y)
            new_area = length*height
            if new_area > area:
                area = new_area
                center_x = vertices[0].x + (length/2)
                center_y = vertices[0].y + (height/2)
                return center_x,cent
            er_y

#function for knowing if the person has chosen right or left            
def decision_maker(new,old):
    if (new-old) > 0.3:
        print("picked left")
        return 1
    elif (new-old) < - 0.3:
        print("picked right")
        return -1
    else:
        print("none chosen")
        return 0

#function for the choices (eg. hot or cold)
def offer_choice(screen, choice1, choice2):
    print('{} or {}?'.format(choice1, choice2))
    screen.askQuestion(choice1, choice2)

# this is steve detecting a person and what starts the interaction 
def person(image):
    response = client.face_detection(image=image)
    face_content = response.face_annotations
    print (face_content)
    
    if face_content and face_content[0].detection_confidence > 0.25:
        print("I see a person(): {}".format(face_content[0].detection_confidence))
        #move the motors 
        my_servo.angle = 10
        return True
    else:
        print("I do not see a person(): No Face Detected at High Confidence!")
        my_servo.angle = 0
        return False

# these are defining the functions that will be executed when called
def steve_waiting(image):
    #steve's "waiting period" between options
    my_servo.angle = 15
    time.sleep(1)

def options(image):
    # I don't think this while loop needs to be here -> while bounding_box == bounding_box_size_at_start # these aren't defined yet 
    servo[0].angle = 70
    servo[1].angle = 60

def selection_right(screen, selection_text): 
    # the arm movements for steve when a selection has been made  
    # if the bb functions returns x == right 
    servo[0].angle = 80
    time.sleep (2)
    servo[1].angle = 0
    time.sleep (3)
    servo[0].angle = 0
    #After moving the arm, print the text to the LCD screen 
    screen.answerQuestion(selection_text)

def selection_left(screen, selection_text)):
    # if the bb function returns x == left 
    servo[1].angle = 80
    time.sleep (2)
    servo[0].angle = 0
    time.sleep (3)
    servo[1].angle = 0
    print(selection_text)
    #After moving the arm, print the text to the LCD screen 
    screen.answerQuestion(selection_text)

       
def driver(screen, left_question, right_question, left_answer, right_answer):
    #this is where things start to happen 
    camera = picamera.PiCamera()
    #take a photo 
    take_photo(camera)
    person_seen = False
    # loop until it sees face
    while person_seen is False:
        #take a new photo, and update variable `image`
        take_photo(camera)
        #check if the person is in this image 
        person_seen = person(image)
        #wait 3 seconds (to not overwhelm the camera)
        time.sleep(3)
    # proceed
    # define the location and size of the bounding box  
    x, y = localize_objects(image)
    
    
    #then present the options and print them to the screen
    print ("Offering a choice ...")
    offer_choice(screen, left_question, right_question)
    print ("Offered a choice.")
    
    #wait for 2 seconds 
    time.sleep(2)
    
    # loop until it detects a valid response 
    detected_a_response = False
    while detected_a_response is False:
        #take a new photo, and update variable `image`
        take_photo(camera)
        #check if the person is in this image 
        person_seen = person(image)
        if person_seen == False: 
            continue
        #wait 1 seconds (to not overwhelm the camera)
        time.sleep(1)
        #find the new position of the object 
        new_x, new_y = localize_objects(image)
        print new_x, new_y
        # respond based on the right or left expansion of the bounding box with a motor output
        res_x = decision_maker(new_x, x)
        if res_x == 1 or res_x is -1: 
            detected_a_response = True
            print "detected a response!"
    
    #done looping, detected a response         
    if res_x == 1:
        print "user moved left"
        selection_left(screen, left_answer)
    elif res_x == -1:
        print "user moved right"
        selection_right(screen, right_answer)
    
    #reset to 10 degrees     
    my_servo.angle = 10

class LCD:
    def __init__(self):
        self.setup()

    def setup(self):
        global lcd
        lcd_rs = digitalio.DigitalInOut(board.D26)
        lcd_en = digitalio.DigitalInOut(board.D19)
        lcd_d7 = digitalio.DigitalInOut(board.D27)
        lcd_d6 = digitalio.DigitalInOut(board.D22)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d4 = digitalio.DigitalInOut(board.D25)

        lcd_columns = 16
        lcd_rows = 2

        import adafruit_character_lcd.character_lcd as characterlcd
        self.lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
        self.lcd.clear()

    def askQuestion(self, option1, option2, bottomText="  Point to one  "):
        self.lcd.clear()
        if len(option1) + len(option2) > 11:
            print("Combined text length cannot be more than 11")
            return
        if len(bottomText) > 16:
            print("Bottom text cannot be more than 16")
            return
        gap = 12 - (len(option1) + len(option2))
        msg = "< " + option1
        for i in range(gap):
            msg += " "
        msg += option2 + " >\n" + bottomText
        self.lcd.message = msg
        
    def answerQuestion(self, answer): 
        self.lcd.clear()
        self.lcd.message = answer

    def clear(self):
        self.lcd.clear()
    #TODO: this is a duplicate of answerQuestion. 
    #this should probably be removed. 
    def showCustomMessage(self, msg):
        self.clear()
        self.lcd.message = msg


def main():
    #initialize LCD
    steveScreen = LCD()
    print ("I'm Steve! I'm here to help.")
    # LCD Prompt 1
    driver(steveScreen, "Hot", "Cold", "You chose hot", "You chose cold")
    time.sleep(2)
    # LCD Prompt 2
    driver(steveScreen, "Coffee",  "Not", "You chose coffee", "You're not human!")
    time.sleep(2)
    # LCD Prompt 3
    driver(steveScreen, "Milk?", "Plain", "You chose not milk" )
    print ("DONE!")
    
if __name__ == '__main__':
        main() 
