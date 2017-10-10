from .nomenclature import UpperBody , LowerBody

class UpperBodyIdentifier:
	pass

class LowerBodyIdentifier:
	pass

class ChestAndBackFilter():
	filters = [
				{
					"filter" : UpperBody.chest(),
					"count" : 5,
					"part" : UpperBodyIdentifier,
				},
				{
					"filter" : UpperBody.back(),
					"count" : 5,
					"part" : UpperBodyIdentifier
				}
			]

class ShouldersAndArmsFilter():
	filters = [
				{
					"filter" : UpperBody.shoulder(),
					"part" : UpperBodyIdentifier,
					"count" : 5
				},
				{
					"filter" : UpperBody.biceps(),
					"part" : UpperBodyIdentifier,
					"count" : 3
				},
				{
					"filter" : UpperBody.triceps(),
					"part" : UpperBodyIdentifier,
					"count" : 2
				}
			]

class AbdomenAndLegsFilter():
	filters = [
				{
					"filter" : UpperBody.abdomen(),
					"part" : UpperBodyIdentifier,
					"count" : 5
				},
				{
					"filter" : LowerBody.legs(),
					"part" : LowerBodyIdentifier,
					"count" : 5
				}
			]

class UpperBodyFilter():
	filters = [

					{
						"filter" : i(),
						"part" : UpperBodyIdentifier,
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

