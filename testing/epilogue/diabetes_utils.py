from weasyprint import HTML
from .views import GuestPDFView , custom_strftime
from django.template.loader import render_to_string
from django.utils.timezone import localdate 
import json



def add_quantity_key(a):
    if a.get('quantity') is None:
        a['quantity'] = 0
    return a

def filter_meal(data , meal):
    return list(filter(lambda x : x.get('meal_type') == meal , data))

def load_file(cals = 0 , day = 0):
    assert cals > 0
    assert day > 0

    with open('disease-data/diabetes-%s-%s.json'%(cals , day)) as f:
        a = json.load(f)
    a = list(map(add_quantity_key , a))

    return {
        "m0" : filter_meal(a,"m0"),
        "m1" : filter_meal(a,"m1"),
        "m2" : filter_meal(a,"m2"),
        "m3" : filter_meal(a,"m3"),
        "m4" : filter_meal(a,"m4"),
        "m5" : filter_meal(a,"m5"),
        "m6" : filter_meal(a,"m6"),
    }

def render_pdf_string(cals = 0 , day = 0 , user = None):
    assert cals > 0
    assert day > 0
    assert user is not None

    meal_data = load_file(cals , day)
    data = {
        **meal_data , 
        "user" : user,
        "intake" : cals,
    }

    return render_to_string("guest-diet-diabetes.html" , data)

def get_pdf(cals = 0 , day = 0 , user = None):
    string = render_pdf_string(cals = cals , day = day , user = user)
    html = HTML(string = string).write_pdf()
    return GuestPDFView.upload_to_s3(html)
