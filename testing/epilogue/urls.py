from django.conf.urls import url
from .views import get_analysis , UserView , DietPlanView

urlpatterns = [
	url(r'analysis' , get_analysis),
	url(r'users/(?P<pk>[0-9]+)/$' , UserView.as_view()),
	url(r'dietplans/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , DietPlanView.as_view())
]