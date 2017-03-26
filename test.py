from dietplan.goals import Goals
from dietplan.utils import annotate_food
from dietplan.models import Food

import heapq ,copy



l = annotate_food(Food.m1_objects , Goals.WeightLoss)
