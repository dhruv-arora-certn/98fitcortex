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

	drink = mongoengine.IntField()
	dairy = mongoengine.IntField()
	snaks = mongoengine.IntField()

	squared_diff = 0

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

	def amplify(self , factor):
		self.weight = self.weight*2
		self.calarie = self.calarie*2
		return self

	@property
	def calorie(self):
		return self.calarie

	@mongoengine.queryset.queryset_manager
	def m1_objects(doc_cls , queryset):
		return queryset.filter(m1 = 1)

	@mongoengine.queryset.queryset_manager
	def m2_objects(doc_cls , queryset):
		return queryset.filter(m2 = 1)

	@classmethod
	def set_context(self, context):
		self.context = context

	def __lt__(self , other):
		return self.squared_diff < other.squared_diff

	def __str__(self):
		return self.name + " " + str(self.squared_diff) 