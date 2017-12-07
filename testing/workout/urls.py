from django.conf.urls import url
from workout.views import WarmupView , StretchingView , CoolDownView ,\
		NoviceCoreView , CardioView , WorkoutView , DashboardWorkoutTextView ,\
		CustomerInjuryView, GenerateWorkoutView

urlpatterns = [
	url(r"^warmup/" , WarmupView.as_view()),
	url(r"^cardio/" , CardioView.as_view()),
	url(r"^core/" , NoviceCoreView.as_view()),
	url(r"^stretching/" , StretchingView.as_view()),
	url(r"^cooldown/" , CoolDownView.as_view()),
	url(r'^workoutplan/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , WorkoutView.as_view()),
	url(r'^workoutplan-new/(?P<year>(2017|2018))/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , GenerateWorkoutView.as_view()),
	url(r'^dashboard/string/' , DashboardWorkoutTextView.as_view()),
	url(r'^injuries/$' , CustomerInjuryView.as_view()),
]
