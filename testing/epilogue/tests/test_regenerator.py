from epilogue.models import Customer
from epilogue.regenerators import DayRegenator, VegRegenerator


c = Customer.objects.get(email = "xsschauhan@gmail.com")
d = VegRegenerator(c, 3, 21, 2018)
