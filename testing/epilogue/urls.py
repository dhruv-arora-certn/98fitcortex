from django.conf.urls import url
from .views import get_analysis

urlpatterns = [
	url(r'analysis' , get_analysis)
]