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

	m5_loss = mongoengine.IntField()
	m5_gain = mongoengine.IntField()
	m5_stable = mongoengine.IntField()
	
	fruit = mongoengine.IntField()
	drink = mongoengine.IntField()
	dairy = mongoengine.IntField()
	snaks = mongoengine.IntField()
	vegetable = mongoengine.IntField()
	cereal_grains = mongoengine.IntField()
	salad = mongoengine.IntField()
	yogurt = mongoengine.IntField()
	dessert = mongoengine.IntField()
	pulses = mongoengine.IntField()
	for_loss = mongoengine.IntField()
	cuisine = mongoengine.StringField()

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
		return round(self.calarie)

	@mongoengine.queryset.queryset_manager
	def m1_objects(doc_cls , queryset):
		return queryset.filter(m1 = 1).filter( calarie__gt = 0)	

	@mongoengine.queryset.queryset_manager
	def m2_objects(doc_cls , queryset):
		return queryset.filter(m2 = 1).filter( calarie__gt = 0)	

	@mongoengine.queryset.queryset_manager
	def m3_objects(doc_cls , queryset):
		return queryset.filter(m3 = 1).filter( calarie__gt = 0)	

	@mongoengine.queryset.queryset_manager
	def m4_objects(doc_cls , queryset):
		return queryset.filter(m4 = 1).filter( calarie__gt = 0).filter(cuisine__ne='Combination')

	@mongoengine.queryset.queryset_manager
	def m5loss_objects(doc_cls , queryset):
		return queryset.filter(m5_loss = 1).filter(calarie__gt = 0).filter(cuisine__ne='Combination')
	
	@mongoengine.queryset.queryset_manager
	def m5gain_objects(doc_cls , queryset):
		return queryset.filter(m5_gain = 1).filter(calarie__gt = 0).filter(cuisine__ne='Combination')

	@mongoengine.queryset.queryset_manager
	def m5stable_objects(doc_cls , queryset):
		return queryset.filter(m5_stable = 1).filter(calarie__gt = 0)

	@classmethod
	def set_context(self, context):
		self.context = context

	def __lt__(self , other):
		return self.squared_diff < other.squared_diff

	def __str__(self):
		return self.name + " " + str(self.squared_diff)

	def update(self , factor):
		self.weight = self.weight * factor
		self.protein = self.protein * factor
		self.fat = self.fat * factor
		self.carbohydrates = self.carbohydrates * factor
		self.calarie = self.calarie*factor
		return self