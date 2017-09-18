from django.dispatch import Signal
from django.dispatch import receiver
from .utils import EmailMessage
from django.template.loader import render_to_string

navratri_signup = Signal(
	providing_args = ["email" , "url" , "lang"]
)

@receiver(navratri_signup)
def send_navratri_email(sender , **kwargs):
	email  = kwargs.pop('email')
	url  = kwargs.pop('url')
	lang = kwargs.pop("lang")

	if lang == "hi":
		template = "navratri-welcome-hindi.html"
		subject = "नवरात्रि व्रत में वजन घटाने के लिए सामग्री की सूची | 98Fit"
	else:
		template = "navratri-welcome-email.html"
		subject = "Your Navratri Ingredient List to lose weight while fasting | 98Fit"

	e = EmailMessage(
		subject = subject,
		message = render_to_string(template , {
			"url" : url
		}),
		recipient = [email],
		html = True
	)
	e.send()

