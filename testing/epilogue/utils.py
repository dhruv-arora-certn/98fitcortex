from datetime import datetime


def get_week(date):
	return date.isocalendar()[1]

def get_day(date):
	return date.isocalendar()[2]


class BulkDifferential:

	def getToDelete(self , old , new):
		old_names = [getattr(e , self.BulkMeta.attr_name) for e in old]
		new_names = [getattr(e , self.BulkMeta.attr_name) for e in new]

		common = []
		for e in old:
			if not getattr(e , self.BulkMeta.attr_name) in new_names:
				common.append(e)
		return common

	def getToAdd(self , old , new):
		old_names = [ getattr(e , self.BulkMeta.attr_name) for e in old]
		new_names = [ getattr(e , self.BulkMeta.attr_name) for e in new]

		common = []
		for e in new:
			if not getattr(e , self.BulkMeta.attr_name) in old_names:
				common.append(e)
		return common	