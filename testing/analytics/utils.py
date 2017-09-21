from .models import UserSignupSource
from epilogue.models import Customer
from django.template.loader import render_to_string



def send_navratri_day_email(self):
	user_list = UserSignupSource.objects.values("customer__email" , "customer__first_name" , flat =True)
	for e in user_list:
		em = EmailMessage(
			subject = "Day 1 Healthy Navratri Diet Plan | 98Fit",
			recipient = [e['customer__email']],
			message = render_to_string("navratri-day-1.html")
		)
	return user_list
