from django.conf.urls import url
from .views import get_analysis , UserView , DietPlanView , DishReplaceView , MealReplaceView , CustomerFoodExclusionView , CustomerMedicalConditionsView , CreateCustomerView , HelloPDF

urlpatterns = [
	url(r'^analysis' , get_analysis),
	url(r'^users/(?P<pk>[0-9]+)/$' , UserView.as_view()),
	url(r'^users/$' , CreateCustomerView.as_view()),
	url(r'^dietplans/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , DietPlanView.as_view()),
	url(r'^dish-replace/(?P<pk>[0-9]+)/$' , DishReplaceView.as_view()),
	url(r'^meal-replace/(?P<week_id>\d{1,55})/(?P<day>[1-7])/(?P<meal>(m1|m2|m3|m4|m5))' , MealReplaceView.as_view()),
	url(r'^food-exclusion/' , CustomerFoodExclusionView.as_view()),
	url(r'^user/medical-condition/$' , CustomerMedicalConditionsView.as_view()),
	url(r'^hello.pdf' , HelloPDF.as_view())
]