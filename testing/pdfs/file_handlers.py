import boto3
import uuid
import os
import datetime


class S3Handler:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id = os.environ.get("S3_ACCESS_KEY"),
            aws_secret_access_key = os.environ.get("S3_ACCESS_SECRET"),
            region_name="ap-south-1"
        )
        self.handler = self.session.resource("s3")

class _S3PDFHandler(S3Handler):

    BucketName = "98fit-guest-diet-pdfs"
    BaseURL = "https://s3.ap-south-1.amazonaws.com/98fit-guest-diet-pdfs/%s"

    def get_bucket(self):
        self.bucket =  self.handler.Bucket(
            self.BucketName
        )
        return self.bucket

    def get_filename(self):
        return '/'.join([
            str(uuid.uuid4()),
            "98fit_Diet_Plan_%s.pdf" % (datetime.datetime.today().strftime("%Y-%m-%d")),
        ])

    def upload(self , data , acl = "public-read" , expires = datetime.datetime.now() + datetime.timedelta(seconds = 60) , content_type = None , content_disposition = None):
        key = self.get_filename()
        bucket = self.get_bucket()

        obj = bucket.put_object(
            Key = key,
            Body = data,
            ACL = acl,
            Expires = expires,
            ContentType = content_type,
            ContentDisposition = content_disposition
        )
        if obj:
            return self.BaseURL%key

class _FileHandler:

	BaseLocation = "/var/tmp/%s.%s"

	def get_filename(self , filename = None , extension = "txt"):
		if not filename:
			filename = str(uuid.uuid4())
		return self.BaseLocation%(filename , extension)

	def save(self , data ,filename = None ,extension = "txt"):
		filename = self.get_filename(filename , extension)
		with open(filename , "wb") as f:
			f.write(data)
		return filename

S3PDFHandler = _S3PDFHandler()
FileHandler = _FileHandler()
