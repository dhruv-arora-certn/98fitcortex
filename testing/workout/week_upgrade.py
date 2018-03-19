from workoutplan import levels

def get_current_fitness(user):
    '''
    Return the current fitness level of the user
    '''
    return user.level_obj

def get_current_weeks(user):
    '''
    Return the Current workout week of the user for his current fitness level
    '''
    return user.user_relative_workout_week


class ComparableRange():

    def __init__(self,start = 0, stop = 0 , step = 1):
        self.start = start
        self.stop = stop
        self.step = step
        self.idx = start - step 
        self.right_boundary = self.stop - 1
        self.left_boundary = self.start

    def __contains__(self,other):
        return self.start <= other < self.stop

    def __le__(self,other):
        assert type(other) in [int,float] , "Cannot Compare"
        return self.left_boundary < other
    
    def __ge__(self,other):
        assert type(other) in [int,float] , "Cannot Compare"
        return self.right_boundary >= other

    def __lt__(self,other):
        assert type(other) in [int,float] , "Cannot Compare"
        return self.left_boundary < other

    def __gt__(self,other):
        assert type(other) in [int,float] , "Cannot Compare"
        return self.right_boundary > other

    def __next__(self):
        self.idx += self.step
        if not self.idx < self.stop:
            raise StopIteration
        return self.idx

    def __repr__(self):
        return "ComparableRange(%d,%d)"%(self.start,self.stop)

    def __iter__(self):
        return self

class InfRange(ComparableRange):
    '''
    Mock the range object with infinite number of iterations
    '''
    def __init__(self, start = 0, step = 1):
        super().__init__(start = start, stop = float('inf'), step = step)

    def __contains__(self,num):
        if num >= self.start:
            return True

    def __repr__(self):
        return "InfRange(%d,%0.1f)"%(self.start,self.stop)

    

week_range_mapping = {
    levels.Novice : ComparableRange(1,7) ,
    levels.Beginner: ComparableRange(7,25),
    levels.Intermediate : InfRange(25)
}

def valid_fitness(week):
    '''
    Return the Valid Fitness Level of the User based on his week
    '''
    mapping = [
        week in v for v in week_range_mapping.values()
    ]
    idx = mapping.index(True)
    return list(week_range_mapping.keys())[idx]

def upgrade(user):
    '''
    Upgrade the user to the next Fitness level
    '''

    current_week = get_current_weeks(user)
    current_fitness = get_current_fitness(user)

    correct_fitness = valid_fitness(current_week)
    
    return correct_fitness == valid_fitness 


