from django.urls import re_path
from authentication.views import RegistrationView,AccountAssociationView , GoogleLoginView , FacebookLoginView , BatraGoogleLoginView, DeviceRegistrationView

urlpatterns = [
	re_path(r'^register/$' , RegistrationView.as_view()),
	re_path(r'^associate/$' , AccountAssociationView.as_view()),
	re_path(r'^google/$' , GoogleLoginView.as_view()),
	re_path(r'^campaign-register/$' , BatraGoogleLoginView.as_view()),
	re_path(r'^facebook/$' , FacebookLoginView.as_view()),
	re_path(r'^device/$' , DeviceRegistrationView.as_view()),
]
