

def body_part_decorator( part ):
	def decorator(cls):
		def applyFilter():
			cls.bodyPartInFocus = part
			return cls
		return applyFilter()
	return decorator
