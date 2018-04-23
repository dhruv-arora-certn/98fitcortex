from django.urls import re_path
from authentication import views

urlpatterns = [
    re_path(r'^register/$' , views.RegistrationView.as_view()),
    re_path(r'^associate/$' , views.AccountAssociationView.as_view()),
    re_path(r'^google/$' , views.GoogleLoginView.as_view()),
    re_path(r'^campaign-register/$' , views.BatraGoogleLoginView.as_view()),
    re_path(r'^facebook/$' , views.FacebookLoginView.as_view()),
    re_path(r'^device/$' , views.DeviceRegistrationView.as_view()),
    re_path(r'^verify-email/$', views.EmailVerificationView.as_view()),
    re_path(r'^resend-verify-email/$', views.EmailVerificationResendView.as_view()),
    re_path(r'^forgot-password-otp/$', views.OTPSendView.as_view()),
    re_path(r'^change-password/$', views.ChangePasswordView.as_view())
]
