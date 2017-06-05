from django import template
import requests , base64

register = template.Library()

@register.filter
def get64(url):
	print("URL  -----" , url)
	if url.startswith("http"):
		string = base64.b64encode(requests.get(url).content).decode("utf-8")
		return str("data:image/png;base64," + string)
	return url