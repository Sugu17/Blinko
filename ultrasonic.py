import RPi.GPIO as GPIO
import time
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor
class Ultra:

    def __init__(self,name,trigger,echo):

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        self.name=name

        #set pin role
        print(f"\nPin {trigger} set as trigger.")
        print(f"\nPin {echo} set as echo.")
        self.trigger=trigger
        self.echo=echo

        self.set_pin_direction()

    def set_pin_direction(self):
        #set GPIO direction (IN / OUT)
        print("\nSetting pin direction...")
        GPIO.setup(self.trigger,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)

    def distance(self):
        data={}
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
        distance = (TimeElapsed * 34300) / 2
        data["Name"]=self.name
        data["Distance"]=distance
        print("\n")
        pprint(data)

def get_data(inst):
    inst.distance()

if __name__ == '__main__':
    try:
        front=Ultra(name="Front",trigger=2,echo=3)
        right=Ultra(name="Right",trigger=4,echo=14)
        left=Ultra(name="Left",trigger=15,echo=17)
        #right=Ultra(name="Right",trigger=12,echo=13)
        instance_list=[front,right,left]
        while True:
            with ProcessPoolExecutor(8) as executor:               
                executor.map(get_data,instance_list,chunksize=4)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
