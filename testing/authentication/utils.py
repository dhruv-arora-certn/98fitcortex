import boto3


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

