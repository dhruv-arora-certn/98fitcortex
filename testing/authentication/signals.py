from django.dispatch import Signal
from django.dispatch import receiver
from django.template.loader import render_to_string

from . import utils


navratri_signup = Signal(
	providing_args = ["email" , "url" , "lang"]
)

#Signal to use when user registers through mobile
mobile_signup = Signal(
    providing_args = [
        "logincustomer"
    ]
)

email_verification = Signal(
    providing_args = [
        "logincustomer"
    ]
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

	e = utils.EmailMessage(
		subject = subject,
		message = render_to_string(template , {
			"url" : url
		}),
		recipient = [email],
		html = True
	)
	e.send()


@receiver(mobile_signup)
def send_welcome_email(sender, **kwargs):
    '''
    Send welcome email to the user coming through the app
    '''
    login_customer = kwargs.get("logincustomer")
    secret = utils.sign(
        login_customer.email
    )
    link = f'<a href="https://www.98fit.com/confirm/{secret}">Click Here</a>'
    message = f'<p>Welcome to 98Fit</p><p>To verify your email address {link}.</p> <p>Link is only valid for 24 hours'
    e = utils.EmailMessage(
        subject = "Welcome to 98Fit",
        message = message,
        recipient = [login_customer.email],
        html = True
    )
    status = e.send()
    return

@receiver(email_verification)
def send_verification_email(sender, **kwargs):
    login_customer = kwargs.get("logincustomer")
    secret = utils.sign(
        login_customer.email
    )
    link = f'<a href="https://www.98fit.com/confirm/{secret}">Click Here</a>'
    message = f'<p>To verify your email address {link}.</p> <p>Link is only valid for 24 hours'
    e = utils.EmailMessage(
        subject = "Welcome to 98Fit",
        message = message,
        recipient = [login_customer.email],
        html = True
    )
    status = e.send()
    return
