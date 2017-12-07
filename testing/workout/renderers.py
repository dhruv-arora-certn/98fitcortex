from rest_framework import renderers


class WorkoutRenderer(renderers.BaseRenderer):

	media_type = "application/json"
	format = "json"

	def render(self , data , media_type = None , renderer_context = None):
		print(data)
		return {}
