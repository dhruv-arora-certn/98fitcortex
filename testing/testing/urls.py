"""testing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import re_path, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.urls import include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/',  include("epilogue.urls")),
    re_path(r'^auth/' , include("rest_auth.urls")),
    re_path(r'^authentication/' , include("authentication.urls")),
    re_path(r'^cheese/' , include("analytics.urls")),
    re_path(r'^workout/' , include("workout.urls")),
    re_path(r'^messaging/' , include("messaging.urls")),
    re_path(r'^docs/', include('rest_framework_docs.urls')),
]
urlpatterns += staticfiles_urlpatterns()
