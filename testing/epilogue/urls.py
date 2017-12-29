from django.conf.urls import url
from .views import get_analysis , UserView , DietPlanView , DishReplaceView , MealReplaceView , CustomerFoodExclusionView ,\
 					CustomerMedicalConditionsView , CreateCustomerView , GuestPDFView , DietPlanRegenerationView , UserDietPlanRegenerationView ,\
 					DietPlanMobileView , WaterBulkView  ,SleepWeeklyAggregationView,SleepMonthlyAggregatedView, WaterWeeklyAggregateView,WaterMonthlyAggregateView , \
					LastDaySleepView, MonthlyActivityView , WeeklyActivityView, ActivityLogView , CustomerSleepLoggingView , DashboardMealTextView , CustomerMedicalConditionsMobileView , CustomerFoodExclusionsMobileView , \
					DiseasePDFView , DietPlanYearlyView

urlpatterns = [
	url(r'^analysis' , get_analysis),
	url(r'^users/(?P<pk>[0-9]+)/$' , UserView.as_view()),
	url(r'^users/$' , CreateCustomerView.as_view()),
	url(r'^dietplans/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , DietPlanView.as_view()),
	url(r'^dietplans/(?P<year>(2017|2018))/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , DietPlanYearlyView.as_view()),
	url(r'^dish-replace/(?P<pk>[0-9]+)/$' , DishReplaceView.as_view()),
	url(r'^meal-replace/(?P<week_id>\d{1,55})/(?P<day>[1-7])/(?P<meal>(m1|m2|m3|m4|m5))/$' , MealReplaceView.as_view()),
	url(r'^food-exclusion/$' , CustomerFoodExclusionView.as_view()),
	url(r'^user/medical-condition/$' , CustomerMedicalConditionsView.as_view()),
	url(r'^user/medical-condition/mobile/$' , CustomerMedicalConditionsMobileView.as_view()),
	url(r'^user/food-exclusion/mobile/$' , CustomerFoodExclusionsMobileView.as_view()),
	url(r'^guest-diet-pdf/$' , GuestPDFView.as_view()),
	url(r'^disease-pdf/(?P<day>[1-7])/$' , DiseasePDFView.as_view()),
	url(r'^dietplans/(?P<id>[0-9]+)/regenerate/$' , DietPlanRegenerationView.as_view()),
	url(r'^user/regenerate' , UserDietPlanRegenerationView.as_view()),
	url(r'^dietplans/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/meal/(?P<meal>(m1|m2|m3|m4|m5))/$' , DietPlanMobileView.as_view()),
	url(r'^logging/water/$',WaterBulkView.as_view()),
	url(r'^logging/activity/$',ActivityLogView.as_view()),
	url(r'^logging/sleep/$',CustomerSleepLoggingView.as_view()),
	url(r'^logging/sleep/aggregate/weekly/(?P<week>[0-9]+)/$' , SleepWeeklyAggregationView.as_view()),
	url(r'^logging/sleep/aggregate/monthly/(?P<month>[0-9]+)/$' , SleepMonthlyAggregatedView.as_view()),
	url(r'^logging/sleep/aggregate/last/$' ,LastDaySleepView.as_view()),
	url(r'^logging/water/aggregate/weekly/(?P<week>[0-9]+)/$' , WaterWeeklyAggregateView.as_view()),
	url(r'^logging/water/aggregate/monthly/$' ,WaterMonthlyAggregateView.as_view()),
	url(r'^logging/activity/aggregate/monthly/(?P<month>[0-9]+)/$' ,MonthlyActivityView.as_view()),
	url(r'^logging/activity/aggregate/weekly/(?P<week>[0-9]+)/$' ,WeeklyActivityView.as_view()),
	url(r'^dashboard/strings/meal/$', DashboardMealTextView.as_view())

]
