
def get_day_from_generator(generator , day):
	return getattr(generator , "D%s"%day)
