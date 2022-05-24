from pprint import pprint
import sys
import ipapi
from datetime import datetime

class GPS:
    def __init__(self) -> None:
        self.response=ipapi.location()

    def get_location(self)->dict:
        self.location={}
        self.location["Latitude"]=self.response["latitude"]
        self.location["Longitude"]=self.response["longitude"]
        self.location["Time"]=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.location["Country"]=self.response["country_name"]
        self.location["City"]=self.response["city"]
        self.location["Region"]=self.response["region"]
        self.location["Postal Code"]=self.response["postal"]
        return self.location

if __name__=="__main__":
    try:
        gps=GPS()
    except KeyboardInterrupt:
        sys.exit("Keyboard Interrupt!")
