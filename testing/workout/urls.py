from django.urls import re_path
from workout.views import WarmupView , StretchingView , CoolDownView ,\
		NoviceCoreView , CardioView , WorkoutView , DashboardWorkoutTextView ,\
		CustomerInjuryView, GenerateWorkoutView

urlpatterns = [
	re_path(r"^warmup/" , WarmupView.as_view()),
	re_path(r"^cardio/" , CardioView.as_view()),
	re_path(r"^core/" , NoviceCoreView.as_view()),
	re_path(r"^stretching/" , StretchingView.as_view()),
	re_path(r"^cooldown/" , CoolDownView.as_view()),
	re_path(r'^workoutplan/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , WorkoutView.as_view()),
	re_path(r'^workoutplan-new/(?P<year>(2017|2018))/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , GenerateWorkoutView.as_view()),
	re_path(r'^dashboard/string/' , DashboardWorkoutTextView.as_view()),
	re_path(r'^injuries/$' , CustomerInjuryView.as_view()),
]
