from workoutplan.goals import Goals 
from workoutplan.resistance_data import *
from workoutplan import decorators
from workoutplan import body_part_focus

class Base:
	pass

class Novice(Base):
	name = "novice"


class Beginner(Base):
	name = "beginner"

	class Resistance:

		class WeightLoss(Goals.WeightLoss):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1:
				filters = [
					{
						"filter" : UpperBody.compound().baseQ | LowerBody.compound().baseQ,
						"count" : 5
					}
				]

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2:
				filters = [
					{
					"filter" : UpperBody.compound().baseQ | LowerBody.compound().baseQ,
					"count" : 5
					}
				]

		class MaintainWeight(Goals.MaintainWeight):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(UpperBodyFilter):
				pass
			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(LowerBodyFilter):
				pass

		class WeightGain(Goals.WeightGain):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(ChestAndBackFilter):
				pass

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(AbdomenAndLegsFilter):
				pass

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D3(ShouldersAndArmsFilter):
				pass


class Intermediate(Base):
	name = "intermediate"

	class Resistance:

		class WeightGain(Goals.WeightGain):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(ChestAndBackFilter):
				pass

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D4(ChestAndBackFilter):
				pass

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D3(ShouldersAndArmsFilter):
				pass

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D6(ShouldersAndArmsFilter):
				pass

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(AbdomenAndLegsFilter):
				pass

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D5(AbdomenAndLegsFilter):
				pass

		class WeightLoss(Goals.WeightLoss):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(UpperBodyFilter):
				pass

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(LowerBodyFilter):
				pass

		class MaintainWeight(Goals.MaintainWeight):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(UpperBodyFilter):
				pass

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(LowerBodyFilter):
				pass
