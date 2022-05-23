#!/usr/bin/env python3

from email import message
import email
import os
import mimetypes,getpass
import smtplib
import sys

class Email():

    def __init__(self,sender,reciever) -> None:
        self.sender=sender
        self.reciever=reciever
        self.client="smtp.gmail.com"
        self.passwd="wzpgtxszgnunvhev"
        
        print("SMTP client set to {}.\n".format(self.client))
        self.server=smtplib.SMTP_SSL(self.client)
        print("Logging in...\n")
        #passwd=getpass.getpass("Enter password:")
        self.login=self.server.login(self.sender,self.passwd)
        log_success=(235, b'2.7.0 Accepted')
        if self.login==log_success:
            print("\nLogged in to smtp server.")
        else:
            print("\nError logging in.")
            raise smtplib.SMTPAuthenticationError
  
    def generate_email(self,subject,content,file_path=None):
        self.Message=message.EmailMessage()
        self.Message["From"]=self.sender
        self.Message["To"]=self.reciever
        self.Message["Subject"]=subject
        self.body=content
        self.Message.set_content(self.body)
        if file_path != None:
            file_name=os.path.basename(file_path)
            main_type,_=mimetypes.guess_type(file_path)
            main_type,sub_type=main_type.split('/',1)
            with open(file_path,mode="rb") as file:
                self.Message.add_attachment(file.read(),maintype=main_type,subtype=sub_type,filename=file_name)

    def send_email(self):
        print("\nSending mail to {}...".format(self.reciever))
        send=self.server.send_message(self.Message)
        status_complete={}
        if send==status_complete:
            print("\nMail Sent successfully.")
        else:
            print("\nError sending mail to {}!".format(send))
        #   self.server.quit()

    def generate_error_report(self,subject,content):
        err_report=message.EmailMessage()
        err_report["From"]=self.sender
        err_report["To"]=self.reciever
        err_report["Subject"]=subject
        self.body=content
        err_report.set_content(self.body)
        return err_report

if __name__=="__main__":
    email=Email("sugumar40579@gmail.com","javidfirnas25@gmail.com")
    email.generate_email(subject="Emergency alert!",content="Shri Raghav is currently under Meth (:",
                        file_path="hans.jpg")
    email.send_email()
    email.server.quit()
    sys.exit()
    


