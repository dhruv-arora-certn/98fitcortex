from django.conf.urls import url , include
from authentication.views import RegistrationView,AccountAssociationView , GoogleLoginView , FacebookLoginView , BatraGoogleLoginView

urlpatterns = [
	url(r'^register/$' , RegistrationView.as_view()),
	url(r'^associate/$' , AccountAssociationView.as_view()),
	url(r'^google/$' , GoogleLoginView.as_view()),
	url(r'^campaing-register/$' , BatraGoogleLoginView.as_view()),
	url(r'^facebook/$' , FacebookLoginView.as_view()),
]
