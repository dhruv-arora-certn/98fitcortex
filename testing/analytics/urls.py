from django.conf.urls import url
from analytics.views import CustomerGoogleClientView,CustomerTrackingView , EventPageTrackingView


urlpatterns = [
	url(r'^jerry/$' , CustomerGoogleClientView.as_view() , name = "customer-google-client"),
	url(r'^trail/$' , CustomerTrackingView.as_view() , name = "customer-tracking"),
	url(r'^mousetrap/$' , EventPageTrackingView.as_view() , name = "event-tracking")
]
