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
        self.detect()
        #pprint(self.data)

    def detect(self):
        if self.distance<=100:
            file_name=f"{self.name}_immedaite.wav"
            play(filename=file_name)          

def get_data(inst):
    inst.distance()

def play(filename):
    data,sampling_rate=soundfile.read(filename,dtype='float32')
    sounddevice.play(data,sampling_rate)
    status=sounddevice.wait()


if __name__ == '__main__':
    try:
        front=Ultra(name="Front",trigger=2,echo=3)
        right=Ultra(name="Right",trigger=4,echo=26)
        left=Ultra(name="Left",trigger=20,echo=17)
        back=Ultra(name="Back",trigger=18,echo=27)
        instance_list=[front,right,left,back]
        while True:
            with ProcessPoolExecutor(200) as executor:               
                executor.map(get_data,instance_list,chunksize=100)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
