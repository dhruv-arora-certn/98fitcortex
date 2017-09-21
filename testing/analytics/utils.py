from .models import UserSignupSource
from epilogue.models import Customer
from django.template.loader import render_to_string
from authentication.utils import EmailMessage


def send_navratri_day_email( users = [] , send = True):
	if not users:
		user_list = UserSignupSource.objects.filter(customer__create_on__day = 20 , customer__create_on__month = 9 , customer__create_on__year = 2017).values("customer__email" , "customer__first_name")
	else:
		user_list = users
	l = []
	sent =  []
	for e in user_list:
		if len(e['customer__first_name']):
			name = e['customer__first_name']
		else:
			name = ""
		em = EmailMessage(
			subject = "Day 1 Healthy Navratri Diet Plan | 98Fit",
			recipient = [e['customer__email']],
			message = render_to_string("navratri-day-1.html" , {
				"name" : name 
			}) , 
			html = True
		)
		if send and not e['customer__email'] in sent:
			l.append([e['customer__email'] , em.send()])
			sent.append(e['customer__email'])
		l.append(e['customer__email'])
	return l
