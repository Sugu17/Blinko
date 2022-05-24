import os
from gps import *
from time import *
import time
import threading
 
gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      os.system('clear')
 
      print ()
      print (' GPS reading')
      print ('----------------------------------------')
      print ('Latitude    ' , gpsd.fix.latitude)
      print ('Longitude   ' , gpsd.fix.longitude)
      print ('Time UTC    ' , gpsd.utc,' + ', gpsd.fix.time)
      print ('Altitude (m)' , gpsd.fix.altitude)
      print ('eps         ' , gpsd.fix.eps)
      print ('epx         ' , gpsd.fix.epx)
      print ('epv         ' , gpsd.fix.epv)
      print ('ept         ' , gpsd.fix.ept)
      print ('Speed (m/s) ' , gpsd.fix.speed)
      print ('Climb       ' , gpsd.fix.climb)
      print ('Track       ' , gpsd.fix.track)
      print ('Mode        ' , gpsd.fix.mode)
      print ()
      print ('Sats        ' , gpsd.satellites)
 
      time.sleep(5) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."