from django.dispatch import Signal
from django.dispatch import receiver
from .utils import EmailMessage
from django.template.loader import render_to_string

navratri_signup = Signal(
	providing_args = ["email" , "url"]
)

@receiver(navratri_signup)
def send_navratri_email(sender , **kwargs):
	email  = kwargs.pop('email')
	url  = kwargs.pop('url')

	e = EmailMessage(
		subject = "Your Navratri Food Checklist from 98fit" ,
		message = render_to_string("navratri-welcome-email.html" , {
			"url" : url
		}),
		recipient = [email],
		html = True
	)
	e.send()

