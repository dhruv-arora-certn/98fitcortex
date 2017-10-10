from workoutplan.goals import Goals 
from workoutplan.resistance_data import *

class Base:
	pass

class Novice(Base):
	name = "novice"


class Beginner(Base):
	name = "beginner"

	class Resistance:

		class WeightLoss(Goals.WeightLoss):
			class D1:
				filter = UpperBody.compound().baseQ | LowerBody.compound().baseQ
				count = 5

			class D2:
				filter = UpperBody.compound().baseQ | LowerBody.compound().baseQ
				count = 5

		class MaintainWeight(Goals.MaintainWeight):

			class D1(UpperBodyFilter):
				pass

			class D2(LowerBodyFilter):
				pass

		class WeightGain(Goals.WeightGain):

			class D1(ChestAndBackFilter):
				pass

			class D2(AbdomenAndLegsFilter):
				pass

			class D3(ShouldersAndArmsFilter):
				pass


class Intermediate(Base):
	name = "intermediate"

	class Resistance:

		class WeightGain(Goals.WeightGain):

			class D1(ChestAndBackFilter):
				pass

			class D4(ChestAndBackFilter):
				pass

			class D3(ShouldersAndArmsFilter):
				pass

			class D6(ShouldersAndArmsFilter):
				pass

			class D2(AbdomenAndLegsFilter):
				pass

			class D5(AbdomenAndLegsFilter):
				pass

		class WeightLoss(Goals.WeightLoss):

			class D1(UpperBodyFilter):
				pass

			class D2(LowerBodyFilter):
				pass

		class MaintainWeight(Goals.MaintainWeight):

			class D1(UpperBodyFilter):
				pass

			class D2(LowerBodyFilter):
				pass
