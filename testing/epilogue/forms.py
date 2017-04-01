from django import forms
from django.core import validators
from dietplan.goals import Goals
from dietplan.activity import ActivityLevel
class AnalysisForm(forms.Form):
	height = forms.FloatField(required = True , label = "Height in Meters")
	weight = forms.FloatField(required = True , label = "Weight in Kgs")
	activity_level = forms.ChoiceField(
		choices = [
			(ActivityLevel.sedentary , 'Sedentary'),
			(ActivityLevel.lightly_active , "Light Active"),
			(ActivityLevel.moderately_active , "Moderately Active"),
			(ActivityLevel.very_active , "Very Active"),
			(ActivityLevel.extra_active , "Extra Active")
		]
	)
	goals = forms.ChoiceField(
		choices = [
			( 0 , 'Weight Loss'),
			( 1 , 'Weight Gain'),
			( 2 , 'Maintain Weight'),
			( 3 , 'Muscle Gain' )
		]
	)