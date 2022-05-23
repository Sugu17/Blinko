import RPi.GPIO as GPIO
import time
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor
 
class PiUltra:

    def __init__(self,name,trigger,echo) -> None:
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BOARD)
        self.name=name
        self.set_pin(trigger,echo)
        self.set_pin_direction()
    
    def set_pin(self,trigger,echo):
        #set pin role
        print(f"\nPin {trigger} set as trigger.")
        print(f"\nPin {echo} set as echo.")
        self.trigger=trigger
        self.echo=echo
    
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

        GPIO.output(self.echo, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.trigger) == 0:
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
        pprint(data)
 
if __name__ == '__main__':
    try:
        front=PiUltra(name="Front",trigger=8,echo=7)
        back=PiUltra(name="Back",trigger=10,echo=11)
        right=PiUltra(name="Right",trigger=12,echo=13)
        left=PiUltra(name="Left",trigger=15,echo=16)
        while True:
            with ProcessPoolExecutor(100) as executor:
                executor.map(PiUltra.distance(),front,
                back,right,left,chunksize=250)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
