from django.conf.urls import url
from analytics.views import CustomerGoogleClientView,CustomerTrackingView , EventPageTrackingView


urlpatterns = [
	url(r'^client/$' , CustomerGoogleClientView.as_view() , name = "customer-google-client"),
	url(r'^track/$' , CustomerTrackingView.as_view() , name = "customer-tracking"),
	url(r'^event-track/$' , EventPageTrackingView.as_view() , name = "event-tracking")

]
