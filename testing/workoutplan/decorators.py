import functools

def body_part_decorator( part ):
	def decorator(cls):
		def applyFilter():
			cls.bodyPartInFocus = part
			return cls
		return applyFilter()
	return decorator

#def buildRegister(priority):
#	def decorator(f):
#		@functools.wraps(f)
#		def wrapper(*args , **kwargs):
#			if not hasattr(obj , registry):
#				obj.registry = []
#			obj.registry.append(f)
#
