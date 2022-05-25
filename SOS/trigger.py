from operator import imod
import RPi.GPIO as GPIO
import sys

class Button:
    def __init__(self,pin) -> None:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.pin=pin
        GPIO.setup(self.pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin,GPIO.RISING,callback=self.button_callback)

    def button_callback(self):
        try:
            print("Pushed")
        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__=="__main":
    button=Button(20)
    sys.exit()
