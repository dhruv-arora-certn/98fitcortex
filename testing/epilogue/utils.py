from datetime import datetime


def get_week(date):
	return date.isocalendar()[1]

def get_day(date):
	return date.isocalendar()[2]