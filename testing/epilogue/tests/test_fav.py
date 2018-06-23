from epilogue.models import *
from epilogue.serializers import *
from epilogue.utils import fav_utils, get_week, get_year


def test_fav_item():
    item = GeneratedDietPlanFoodDetails.objects.last() 
    customer = item.dietplan.customer
    calendar, created = customer.calendar.get_or_create(
        customer = customer,
        year = get_year(),
        week = get_week()
    )
    data = fav_utils.get_item_favourite_details(item, calendar, 1)
    serializer = CustomerDietFavouriteSerializer(data = data, many = True)

    serializer.is_valid(raise_exception = True)


    val = serializer.save()
    return serializer

def test_fav_day():
    customer = Customer.objects.get(pk = 1604)
    qs = GeneratedDietPlanFoodDetails.objects.filter(
        dietplan__customer = customer,
        dietplan__week_id = 25,
        dietplan__year = 2018,
        day = 5,
        meal_type = 'm5'
    )
    calendar, created = customer.calendar.get_or_create(
        week = 25,
        year = 2018
    )

    preference = 1

    data = fav_utils.get_meal_favourite_details(qs, calendar, preference)

    serializer = CustomerDietFavouriteSerializer(
        data = data, many = True
    )
    
    serializer.is_valid(raise_exception = True)

    val = serializer.save()

    return val
