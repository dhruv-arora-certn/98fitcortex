from django.urls import re_path, path
from .views import  UserView , DietPlanView , DishReplaceView , MealReplaceView , CustomerFoodExclusionView ,\
                    CustomerMedicalConditionsView , CreateCustomerView , GuestPDFView , DietPlanRegenerationView , UserDietPlanRegenerationView ,\
                    WaterBulkView  ,SleepWeeklyAggregationView,SleepMonthlyAggregatedView, WaterWeeklyAggregateView,WaterMonthlyAggregateView , \
                    LastDaySleepView, MonthlyActivityView , WeeklyActivityView, ActivityLogView , CustomerSleepLoggingView , DashboardMealTextView , CustomerMedicalConditionsMobileView , CustomerFoodExclusionsMobileView , \
                    DiseasePDFView  , CustomerReasonsView , RegenerableDietPlanView, CustomerPreferenceView, DayRegenerationView, CustomerDietPlanFollowView

from . import views
from rest_framework import routers

urlpatterns = [
    re_path(r'^users/(?P<pk>[0-9]+)/$' , UserView.as_view()),
    re_path(r'^users/$' , CreateCustomerView.as_view()),
    re_path(r'^dietplans/(?P<year>(2017|2018))/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , RegenerableDietPlanView.as_view()),
    re_path(r'^dish-replace/(?P<pk>[0-9]+)/$' , DishReplaceView.as_view()),
    re_path(r'^meal-replace/(?P<year>(2017|2018))/(?P<week_id>\d{1,55})/(?P<day>[1-7])/(?P<meal>(m1|m2|m3|m4|m5))/$' , MealReplaceView.as_view()),
    re_path(r'^food-exclusion/$' , CustomerFoodExclusionView.as_view()),
    re_path(r'^user/medical-condition/$' , CustomerMedicalConditionsView.as_view()),
    re_path(r'^user/medical-condition/mobile/$' , CustomerMedicalConditionsMobileView.as_view()),
    re_path(r'^user/reasons/$' , CustomerReasonsView.as_view()),
    re_path(r'^user/food-exclusion/mobile/$' , CustomerFoodExclusionsMobileView.as_view()),
    re_path(r'^guest-diet-pdf/$' , GuestPDFView.as_view()),
    re_path(r'^disease-pdf/(?P<day>[1-7])/$' , DiseasePDFView.as_view()),
    re_path(r'^dietplans/(?P<id>[0-9]+)/regenerate/$' , DietPlanRegenerationView.as_view()),
    re_path(r'^user/regenerate' , UserDietPlanRegenerationView.as_view()),
    re_path(r'^logging/water/$',WaterBulkView.as_view()),
    re_path(r'^logging/activity/$',ActivityLogView.as_view()),
    re_path(r'^logging/sleep/$',CustomerSleepLoggingView.as_view()),
    re_path(r'^logging/sleep/aggregate/weekly/(?P<week>[0-9]+)/$' , SleepWeeklyAggregationView.as_view()),
    re_path(r'^logging/sleep/aggregate/monthly/(?P<month>[0-9]+)/$' , SleepMonthlyAggregatedView.as_view()),
    re_path(r'^logging/sleep/aggregate/last/$' ,LastDaySleepView.as_view()),
    re_path(r'^logging/water/aggregate/weekly/(?P<week>[0-9]+)/$' , WaterWeeklyAggregateView.as_view()),
    re_path(r'^logging/water/aggregate/monthly/(?P<month>[0-9]+)/$' ,WaterMonthlyAggregateView.as_view()),
    re_path(r'^logging/activity/aggregate/monthly/(?P<month>[0-9]+)/$' ,MonthlyActivityView.as_view()),
    re_path(r'^logging/activity/aggregate/weekly/(?P<week>[0-9]+)/$' ,WeeklyActivityView.as_view()),
    re_path(r'^dashboard/strings/meal/$', DashboardMealTextView.as_view()),
    re_path(r'^food-preference/$', CustomerPreferenceView.as_view()),
    re_path(r'^day-regenerate/(?P<year>(2017|2018))/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$', DayRegenerationView.as_view()),
    re_path(r'^diet-follow/(?P<year>(2017|2018))/(?P<week>[0-9]+)/day/(?P<day>[1-7])/$', CustomerDietPlanFollowView.as_view())
]

diet_fav_urlpatterns = [
    path('favourite/item/<int:pk>', views.CustomerItemFavouriteView.as_view()),
    path('favourite/meal/', views.CustomerMealFavouriteView.as_view())
]

urlpatterns += diet_fav_urlpatterns
