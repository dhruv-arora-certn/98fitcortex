from .activity import ActivityLevel
import lego

class BMIClassificationBase:
    upper = 100
    lower = 0

    @classmethod
    def is_true(self , bmi):
        self.truth = self.lower <= bmi < self.upper 
        return self.truth

    @classmethod
    def number(self , activity):
        if activity == ActivityLevel.sedentary:
            return self.sedentary
        if activity == ActivityLevel.lightly_active:
            return self.lightly_active
        if activity == ActivityLevel.moderately_active:
            return self.moderately_active
        if activity == ActivityLevel.very_active:
            return self.very_active
        if activity == ActivityLevel.extra_active:
            return self.extra_active

    def __str__(self):
        return self.__name__


class BMI:
    class UnderWeight(BMIClassificationBase):
        upper = 18.5
        sedentary = 30
        lightly_active = 32
        moderately_active = 35
        very_active = 37
        extra_active = 40

    class NormalWeight(BMIClassificationBase):
        lower = 18.5
        upper = 22.9
        sedentary = 25
        lightly_active = 27
        moderately_active = 30
        very_active = 32
        extra_active = 35

    class OverWeight(BMIClassificationBase):
        lower = 23
        upper = 27
        sedentary = 20
        lightly_active = 22
        moderately_active = 25
        very_active = 27
        extra_active = 30

    class Obese(BMIClassificationBase):
        lower = 27
        upper = 50
        sedentary = 20
        lightly_active = 22
        moderately_active = 25
        very_active = 27
        extra_active = 30
    
    classifications = [OverWeight , NormalWeight , UnderWeight , Obese]
    # #l@ego.assemble.assemble
    def __init__(self , weight, height):
        self.bmi = self.weight/self.height**2
    
    @property
    def category(self):
        return [e for e in self.classifications if e.is_true(self.bmi)].pop()
