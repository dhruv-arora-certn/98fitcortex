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
			class D1(UpperBodyFilter):
				reps = 12
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(LowerBodyFilter):
				reps = 12
				sets = 3

		class MaintainWeight(Goals.MaintainWeight):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(UpperBodyFilter):
				reps = 15
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(LowerBodyFilter):
				reps = 15
				sets = 3

		class WeightGain(Goals.WeightGain):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(ChestAndBackFilter):
				reps = 12
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(AbdomenAndLegsFilter):
				reps = 12
				sets = 3

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D3(ShouldersAndArmsFilter):
				reps = 12
				sets = 3

		class MuscleGain(Goals.WeightGain):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(ChestAndBackFilter):
				reps = 12
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(AbdomenAndLegsFilter):
				reps = 12
				sets = 3

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D3(ShouldersAndArmsFilter):
				reps = 12
				sets = 3

class Intermediate(Base):
	name = "intermediate"

	class Resistance:

		class WeightGain(Goals.WeightGain):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(ChestAndBackFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D4(ChestAndBackFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D3(ShouldersAndArmsFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D6(ShouldersAndArmsFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(AbdomenAndLegsFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D5(AbdomenAndLegsFilter):
				reps = 10
				sets = 3

		class MuscleGain(Goals.WeightGain):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(ChestAndBackFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D4(ChestAndBackFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D3(ShouldersAndArmsFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D6(ShouldersAndArmsFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(AbdomenAndLegsFilter):
				reps = 10
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D5(AbdomenAndLegsFilter):
				reps = 10
				sets = 3

		class WeightLoss(Goals.WeightLoss):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(UpperBodyFilter):
				reps = 15
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(LowerBodyFilter):
				reps = 15
				sets = 3

		class MaintainWeight(Goals.MaintainWeight):

			@decorators.body_part_decorator(body_part_focus.UpperBody)
			class D1(UpperBodyFilter):
				reps = 12
				sets = 3

			@decorators.body_part_decorator(body_part_focus.LowerBody)
			class D2(LowerBodyFilter):
				reps = 12
				sets = 3
