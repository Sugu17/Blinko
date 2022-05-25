from pprint import pprint
import sys
import ipapi

class GPS:
    def __init__(self) -> None:
        self.get_location()

    def get_location(self):
        response=ipapi.location()
        required=[]
        self.location={
            "Latitude":response["latitude"],
            "Longitude":response["longitude"],
            "Country":response["country_name"],
            "City":response["city"],
            "Region":response["region"],
            "Postal Code":response["postal"]
        }
        pprint(self.location)

if __name__=="__main__":
    try:
        gps=GPS()
    except KeyboardInterrupt:
        sys.exit("Keyboard Interrupt!")
