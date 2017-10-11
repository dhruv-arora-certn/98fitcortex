from .nomenclature import UpperBody , LowerBody

class ChestAndBackFilter():
	filters = [
				{
					"filter" : UpperBody.chest(),
					"count" : 5,
				},
				{
					"filter" : UpperBody.back(),
					"count" : 5,
				}
			]

class ShouldersAndArmsFilter():
	filters = [
				{
					"filter" : UpperBody.shoulder(),
					"count" : 5
				},
				{
					"filter" : UpperBody.biceps(),
					"count" : 3
				},
				{
					"filter" : UpperBody.triceps(),
					"count" : 2
				}
			]

class AbdomenAndLegsFilter():
	filters = [
				{
					"filter" : UpperBody.abdomen(),
					"count" : 5
				},
				{
					"filter" : LowerBody.legs(),
					"count" : 5
				}
			]

class UpperBodyFilter():
	filters = [

					{
						"filter" : i(),
						"count" : e
					}
					for i,e in UpperBody.groups()

			]

class LowerBodyFilter():
	filters = [
				{
					"filter" : i,
					"count" : e
				}
				for i,e in LowerBody.groups()
			]

