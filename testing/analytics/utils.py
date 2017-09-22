from .models import UserSignupSource
from epilogue.models import Customer
from django.template.loader import render_to_string
from authentication.utils import EmailMessage
from django.utils.timezone import localtime , now

def send_navratri_day_email( users = [] , send = True):
	d = localtime(now()).date()
	if not users:
		user_list = UserSignupSource.objects.filter(customer__create_on__lt = d)
	else:
		user_list = users
	l = []
	sent =  []
	for e in user_list:
		if len(e.customer.first_name):
			name = e.customer.first_name
		else:
			name = ""

		if e.language == "hi":
			template = "day-2-hindi.html"
			subject = "सेहतमंद नवरात्रि डाइट प्लान का तीसरा दिन | 98fit"
		else:
			template = "day-3.html"
			subject = "Day 3 Healthy Navratri Diet Plan | 98Fit"

		em = EmailMessage(
			subject = subject,
			recipient = [e.customer.email],
			message = render_to_string(template , {
				"name" : name 
			}) , 
			html = True
		)
		if send and not e.customer.email in sent:
			l.append([[e.customer.email] , em.send()])
			sent.append(e.customer.email)
		l.append(e.customer.email)
	return l
