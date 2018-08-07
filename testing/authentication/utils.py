import boto3
import random

from django.core import signing


class EmailMessage():
    
    def __init__(self , subject = None , message = None , recipient = [] , sender = "98Fit<info@98fit.com>" , html = False):
        self.subject = subject  
        self.message = message
        self.recipient = recipient
        self.sender = sender
        self.html = html

    def get_message_object(self):
        return {
            "Subject" : self.get_subject_object() ,
            "Body" : self.get_body_object()
        }

    def get_destination_object(self):
        return {
            "ToAddresses" : self.recipient
        }
    
    def get_source(self):
        return self.sender  

    def get_subject_object(self):
        return {
            "Data" : self.subject
        }
    
    def get_body_object(self):
        message = {
            "Data" : self.message
        }

        if self.html:
            return {
                'Html' : message

            }

        return {
            "Text" : message
        }   

    def get_client(self):
        return  boto3.client(
            "ses",
            aws_access_key_id = "AKIAIGH4FX24ZSFPKRSA",
            aws_secret_access_key = "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",
            region_name = "us-west-2"
            )

    def send(self):
        client = self.get_client()
        return client.send_email(
            Source = self.get_source(),
            Destination = self.get_destination_object(),
            Message = self.get_message_object()
        )


def sign(data = None, signer = signing.TimestampSigner):
    '''
    Sign data 

    Params
    ------
    data : data to sign
    signer : signer to use
    '''
    signer = signer()
    value = signer.sign(data) 
    return value

def unsign(value, signer = signing.TimestampSigner, max_age = 0):
    '''
    Unsign data

    Params
    ------
    value: data to unsign
    signer: signer to use to unsign
    max_age: maximum age of the data
    '''
    signer = signer()
    value = signer.unsign(value, max_age=max_age)
    return value


def get_otp():
    '''
    Generate a 4 digit random number
    '''
    return random.randint(999,9999)

def get_signed_otp(otp,email):
    '''
    Sign the OTP using object signing
    '''
    return signing.dumps({
        "otp" : otp,
        "email" : email
    })

def otp_email_from_signature(signature):
    return signing.loads(signature, max_age = 300)

def verify_otp_signature(signature, otp, email):
    '''
    Verify if the otp and email in signature match the given params
    '''
    signature = otp_email_from_signature(signature)
    if signature['otp'] == otp and signature['email'] == email:
        return True
    return False
    
