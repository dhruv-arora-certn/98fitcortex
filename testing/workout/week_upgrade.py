from workoutplan import levels

import logging
import collections


logger = logging.getLogger("fitness_upgrade")

def get_current_fitness(user):
    '''
    Return the current fitness level of the user
    '''
    return user.level_obj


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

    

week_range_mapping = collections.OrderedDict({
    levels.Novice : ComparableRange(1,7) ,
    levels.Beginner: ComparableRange(1,19),
    levels.Intermediate : InfRange(1)
})

call_count = 1
def valid_fitness(current_fitness,week):
    '''
    Return the Valid Fitness Level of the User based on his week
    '''
    #If user is intermediate, no need to change the fitness level
    if current_fitness == levels.Intermediate:
        return levels.Intermediate
    
    #If the user 
    #if current_fitness == levels.Beginner:
     #   week -= 6
    
    #If the weeks since last upgrade are in range of current fitness, no need to upgrade
    if not current_fitness == levels.Intermediate and week in week_range_mapping[current_fitness]:
        return current_fitness 
    
    #If the user's weeks are not in range check if the next fitness level is in range

    keys = list(week_range_mapping.keys())
    next_fitness = keys[keys.index(current_fitness) + 1]
    return valid_fitness(next_fitness, week - week_range_mapping[current_fitness].right_boundary) 

def _valid_fitness(current_fitness,week):
    '''
    Return the Valid Fitness Level of the User based on his week
    '''

    mapping = [
        week in v for v in week_range_mapping.values()
    ]
    logger.debug("Mapping for week %d"%(week), mapping)
    idx = mapping.index(True)
    return list(week_range_mapping.keys())[idx]

def upgrade(user , week):
    '''
    Upgrade the user to the next Fitness level
    '''

    current_fitness = get_current_fitness(user)

    correct_fitness = valid_fitness(current_fitness,week)
    
    return correct_fitness, correct_fitness != current_fitness 


