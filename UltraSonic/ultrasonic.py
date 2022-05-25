import RPi.GPIO as GPIO
import time
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor
import emails
import get_gps
import sounddevice,soundfile

class Ultra:

    def __init__(self,name,trigger,echo):

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        self.name=name

        #Initialize mail service
        #self.setup_email()
        #self.gps=get_gps.GPS()

        #set pin role
        print(f"\nPin {trigger} set as trigger.")
        print(f"\nPin {echo} set as echo.")
        self.trigger=trigger
        self.echo=echo
        self.set_pin_direction()

    def setup_email(self):
        sender="sugumar40579@gmail.com"
        receiver="javidfirnas25@gmail.com"
        self.subject="Emergency alert!"
        self.email=emails.Email(sender,receiver)

    def set_pin_direction(self):
        #set GPIO direction (IN / OUT)
        print("\nSetting pin direction...")
        GPIO.setup(self.trigger,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)

    def distance(self):
        self.data={}
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)

        GPIO.output(self.trigger, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
        
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        self.distance = (TimeElapsed * 34300) / 2
        self.data["Name"]=self.name
        self.data["Distance"]=self.distance
        pprint(self.data)
        return(self.data,self.detect())

    def detect(self)->bool:
        if self.distance<=20:
            return True
        else:
            return False

def get_data(inst):
    return inst.distance()

def play(filename):
    data,sampling_rate=soundfile.read(filename,dtype='float32')
    sounddevice.play(data,sampling_rate)
    status=sounddevice.wait()

def process(list):
    front_data,front_value=list[0]
    right_data,right_value=list[1]
    left_data,left_value=list[2]
    back_data,back_value=list[3]
    try:
        if front_value==False and right_value==False and left_value==False and back_value==True:
            file_name="audio/Back_immediate.wav"
            play(file_name)
        elif front_value==False and right_value==False and left_value==True and back_value==False:
            file_name="audio/Left_immediate.wav"
            play(file_name)
        elif front_value==False and right_value==False and left_value==True and back_value==True:
            file_name="audio/Left_and_Back_immediate.wav"
            play(file_name)
        elif front_value==False and right_value==True and left_value==False and back_value==False:
            file_name="audio/Right_immediate.wav"
            play(file_name)
        elif front_value==False and right_value==True and left_value==False and back_value==True:
            file_name="audio/Right_and_Back_immediate.wav"
        elif front_value==False and right_value==True and left_value==True and back_value==False:
            file_name="audio/Right_and_Left_immediate.wav"
            play(file_name)
        elif front_value==False and right_value==True and left_value==True and back_value==True:
            file_name="audio/Right_and_Left_Back_immediate.wav"
            play(file_name)
        elif front_value==True and right_value==False and left_value==False and back_value==False:
            file_name="audio/Front_immediate.wav"
            play(file_name)
        elif front_value==True and right_value==False and left_value==False and back_value==True:
            file_name="audio/Front_and_Back_immediate.wav"
            play(file_name)
        elif front_value==True and right_value==False and left_value==True and back_value==False:
            file_name="audio/Front_and_Left_immediate.wav"
            play(file_name)
        elif front_value==True and right_value==False and left_value==True and back_value==True:
            file_name="audio/Front_and_Left_Back_immediate.wav"
            play(file_name)
        elif front_value==True and right_value==True and left_value==False and back_value==False:
            file_name="audio/Front_and_Right_immediate.wav"
            play(file_name)
        elif front_value==True and right_value==True and left_value==False and back_value==True:
            file_name="audio/Front_and_Right_Back_immediate.wav"
            play(file_name)
        elif front_value==True and right_value==True and left_value==True and back_value==False:
            file_name="audio/Front_and_Right_Left_immediate.wav"
            play(file_name)
        elif front_value==True and right_value==True and left_value==True and back_value==True:
            file_name="audio/Front_and_Right_Left_Back_immediate.wav"
            play(file_name) 
    except UnboundLocalError:
        pass

if __name__ == '__main__':
    try:
        front=Ultra(name="Front",trigger=2,echo=3)
        right=Ultra(name="Right",trigger=4,echo=14)
        left=Ultra(name="Left",trigger=15,echo=17)
        back=Ultra(name="Back",trigger=18,echo=27)
        instance_list=[front,right,left,back]
        while True:
            with ProcessPoolExecutor(200) as executor:
                result=list(executor.map(get_data,instance_list,chunksize=100))
                process(result)
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
