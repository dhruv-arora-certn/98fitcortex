from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^jerry/$' , views.CustomerGoogleClientView.as_view() , name = "customer-google-client"),
	url(r'^trail/$' , views.CustomerTrackingView.as_view() , name = "customer-tracking"),
	url(r'^mousetrap/$' , views.EventPageTrackingView.as_view() , name = "event-tracking"),
        url(r'^feedback/$' , views.UserFeedbackView.as_view() , name = "user-feedback")
]
