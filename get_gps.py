from pigps import GPS
import time

class PiGPS():
    
    def __init__(self) -> None:
        self.gps=GPS()
        self.data={"Latitude":"", "Longitude":"", "Altitude":"", "Time":0}
    
    def get_coordinates(self):
        self.data={}
        self.data["Latitude"]=self.gps.lat
        self.data["Longitude"]=self.gps.lon
        self.data["Altitude"]=self.gps.alt
        self.data["Time"]=self.gps.time
        return self.data

if __name__=="__main__":
    gps=PiGPS()
    gps.get_coordinates()