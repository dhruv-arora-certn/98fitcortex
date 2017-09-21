from .models import UserSignupSource
from epilogue.models import Customer
from django.template.loader import render_to_string



def send_navratri_day_email( send = True):
	user_list = UserSignupSource.objects.filter(customer__create_on__day = 20 , customer__create_on__month = 9 , customer__create_on__year = 2017).values("customer__email" , "customer__first_name")
	l = []
	for e in user_list:
		em = EmailMessage(
			subject = "Day 1 Healthy Navratri Diet Plan | 98Fit",
			recipient = [e['customer__email']],
			message = render_to_string("navratri-day-1.html") , 
			html = True
		)
		if send:
			l.append([e['customer__email'] , em.send()])
		l.append(e['customer__email'])
	return l
