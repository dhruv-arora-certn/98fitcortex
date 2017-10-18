from django.conf.urls import url
from workout.views import WarmupView , StretchingView , CoolDownView , NoviceCoreView , CardioView , WorkoutView

urlpatterns = [
	url(r"^warmup/" , WarmupView.as_view()),
	url(r"^cardio/" , CardioView.as_view()),
	url(r"^core/" , NoviceCoreView.as_view()),
	url(r"^stretching/" , StretchingView.as_view()),
	url(r"^cooldown/" , CoolDownView.as_view()),
	url(r'^workoutplan/(?P<week_id>[0-9]+)/day/(?P<day>[1-7])/$' , WorkoutView.as_view()),
]
