import mongoengine

mongoengine.connect(db = "98fit")

class Food(mongoengine.Document):
	name = mongoengine.StringField()
	quantity = mongoengine.IntField()
	calarie = mongoengine.FloatField()
	serving = mongoengine.IntField()
	weight = mongoengine.IntField()
	fat = mongoengine.FloatField()
	protein = mongoengine.FloatField()
	carbohydrates = mongoengine.FloatField()
	m1 = mongoengine.IntField()
	m2 = mongoengine.IntField()
	m3 = mongoengine.IntField()
	m4 = mongoengine.IntField()

	meta = {
		'collection' : 'food_list',
		'strict' : False
	}

	def pcf_value(self): 
		return sum(
			[ 
				self.protein/protein_ideal,
				self.carbohydrates/carb_ideal,
				self.fat/fat_ideal
			]
		)

	@property
	def calorie(self):
		return self.calarie

	@mongoengine.queryset.queryset_manager
	def objects(doc_cls , queryset):
		return queryset

	@classmethod
	def set_context(self, context):
		self.context = context