#THIS IS TAKEN FROM TEST.PY ON THE PI AS OF SUNDAY MORNING 
#WE GOT THE SERVO MOTOR WORKING AND ARE NOW ADDING THE RESPONSIVITY FUNCTIONS


import picamera     #camera library
import pygame as pg #audio library
import os           #communicate with os/command line

from google.cloud import vision  #gcp vision library
from time import sleep
from adafruit_crickit import crickit
from will_new_LCD_code import LCD
import time
import signal
import sys
import re           #regular expression lib for string searches!

import satcode
import select_drink
import final_sound

#set up your GCP credentials - replace the " " in the following line with your .json file and path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../DET190-JSON/Pinky-DET-2019-e4f4274adb35.json"
# this line connects to Google Cloud Vision! 
client = vision.ImageAnnotatorClient()

# global variable for our image file - to be captured soon!
image = 'image.jpg'

#sounds
on_sound = "/home/pi/DET2019_Class5/pinky_yes_sound.wav"
#complete_sound = "/home/pi/DET2019_Class5/270402__littlerobotsoundfactory__jingle-win-00.wav"

def takephoto(camera):
    
    # this triggers an on-screen preview, so you know what you're photographing!
    camera.start_preview() 
    sleep(0.5)                   #give it a pause so you can adjust if needed
    camera.capture('image.jpg') #save the image
    camera.stop_preview()       #stop the preview
    
def play_on_sound():
    pg.init()
    pg.mixer.init()

    pg.mixer.music.load(on_sound)
    pg.mixer.music.play()

        
def person_seen(image):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    #with open(path, 'rb') as image_file:
    #    content = image_file.read()
    #image = vision.types.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations
    counter = 0
    #print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        #print('\n{} (confidence: {})'.format(object_.name, object_.score))
        if object_.name == 'Person': #if multiple people detected - this will break
            counter += 1
    if counter > 0:
        return True
    else:
        return False
            
def localize_objects(image):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    #with open(path, 'rb') as image_file:
    #    content = image_file.read()
    #image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    #print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
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
                return center_x,center_y
                print(center_x, center_y)

def decision_maker(new,old):
    print(new-old)
    if (new-old)> 0.04:
        print("picked right")
        return "right"
    elif (new-old)<-0.04:
        print("picked left")
        return "left"
    else:
        print("none chosen")
        return "none"

def decision_tracker(chosen, question):
    if chosen == "left":
        return question[1]
    elif chosen == "right":
        return question[0]
    else:
        return "none"

        
def main():
    
    #generate a camera object for the takephoto function to
    #work with
    camera = picamera.PiCamera()
    
    #setup our pygame mixer to play audio in subsequent stages

    #sounds    
    
    takephoto(camera)
    with open('image.jpg', 'rb') as image_file:
        #read the image file
        content = image_file.read()
        #convert the image file to a GCP Vision-friendly type
        image = vision.types.Image(content=content)
        first = person_seen(image)
    time.sleep(2)
    takephoto(camera)
    with open('image.jpg', 'rb') as image_file:
        content = image_file.read()
        #convert the image file to a GCP Vision-friendly type
        image = vision.types.Image(content=content)
        second = person_seen(image)
    if first and second == True:
        seen = True
    else: seen = False
            
    
    #this while loop lets the script run until you ctrl+c (command line)
    #or press 'stop' (Thonny IDE)
    while seen == True:
        #play the on sound
        #pg.mixer.music.load(on_sound)
        #pg.mixer.music.play()
        lcd = LCD()
        lcd.showCustomMessage("Hi! I'm Steve!")
        satcode.steve_sleeping()
        time.sleep(2)
        play_on_sound()
        satcode.steve_sees_you()
        lcd.showCustomMessage("I'm here to help") #this is how you get screen print outs
        questions = [("Hot", "Cold"), ("Coffee", "Tea"), ("Caff.","Decaf"), ("Flavor", "Plain")]
        answers = []
        #takephoto(camera) # First take a picture
        with open('image.jpg', 'rb') as image_file:
            #read the image file
            content = image_file.read()
            #convert the image file to a GCP Vision-friendly type
            image = vision.types.Image(content=content)
            (oldx,oldy) = localize_objects(image)
            time.sleep(1)
        for q in questions:
            lcd.askQuestion(q[0], q[1])
            satcode.steve_gives_options()
            takephoto(camera)
            with open('image.jpg', 'rb') as image_file:
                #read the image file
                content = image_file.read()
                #convert the image file to a GCP Vision-friendly type
                image = vision.types.Image(content=content)
                (x,y)=localize_objects(image)
                decision= decision_maker(x,oldx)
                satcode.steve_recieved_your_choice(decision)
                choices = decision_tracker(decision,q)
                answers.append(choices)
                if decision == "right":
                    lcd.showCustomMessage(q[0])
                elif decision == "left":
                    lcd.showCustomMessage(q[1])
                else:
                    lcd.showCustomMessage("Didn't get\nthat!")
                #(oldx, oldy) = (x,y)
                seen = False
                time.sleep(3)
        answers = [x for x in answers if x != "none"]
        print(answers)
        order = select_drink.your_order(answers)
        print(order)
        lcd.showCustomMessage(order)
        final_sound
        #play_sound(end)
        time.sleep(6)
        lcd.showCustomMessage("Thank You!")
        satcode.steve_sleeping()
        time.sleep(4)
        
        
if __name__ == '__main__':
        main() 
