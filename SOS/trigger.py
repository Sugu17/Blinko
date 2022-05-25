from operator import imod
import RPi.GPIO as GPIO
import sys,time

pin = 20

def setup():
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(pin, GPIO.IN)   

def loop():
        while True:
              button_state = GPIO.input(pin)
              if  button_state == False:
                  print("Button Pressed")
                  while GPIO.input(pin) == False:
                    time.sleep(0.2)
def endprogram():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("keyboard interrupt detected")
        endprogram()