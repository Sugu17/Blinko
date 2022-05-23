#! /usr/bin/env python3
from emails import Email
from get_gps import PiGPS
from pprint import pformat
import sys

sender="sugumar40579@gmail.com"
receiver="javidfirnas25@gmail.com"
subject="Emergency alert!"

if __name__=="__main__":
    email=Email(sender,receiver)
    gps=PiGPS().get_coordinates()
    body=f"Sri Raghav is currently under hallucination, His last seen location was\n{pformat(gps)}"
    email.generate_email(subject,body)
    email.send_email()
    sys.exit()