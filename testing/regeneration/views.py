from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics

from .models import RegenerationLog

import logging

# Create your views here.
class RegenerableView(generics.GenericAPIView):
    """
    This view allows the inheriting classes to regenerate the objects before returning them
    to the API

    Methods
    ------

    get_object(self)
        The entrypoint function for the inheriting class.
        
        Returns the desired object. Regenerates it, if it was marked for regeneration.

    get_regenerate_log_filter(self)
        Get the filters required to get the regeneration object as a dict

        The inheriting class must implement this function

        Returns
        ------
        filter: dict
            Dictionary containing the key-value pairs used 
            for filtering  the regeneration object

    get_object_hook(self)
       Return the original object

       Inheriting class must implement this method

    regeneration_hook(self, obj)
        Function hook to regenerate the object

        The inheriting class must implement this function 

        Parameters
        ---------
        `obj`
            Object which has to be regenerated. Usually instance of `epilogue.models.GeneratedDietPlan` or `workout.models.GeneratedExercisePlan`
        
    """
    logger = logging.getLogger(__name__)

    def get_object_hook(self):
        '''
        Return the object that has to be regenerated
        '''
        raise NotImplementedError("The child class should implement this function")

    def get_regenerate_log_filter(self):
        '''
        Return the dictionary with key-value pairs that will uniquely identify the regeneration log object
        '''
        raise NotImplementedError("The child class should implement this function")

    def regeneration_hook(self, obj):
        '''
        Regenerate the `obj` and return the new object
        '''
        raise NotImplementedError("The child class must implement this function")

    def get_regeneration_log_object(self):
        '''
        Get the models.RegenerationLog instance based on the filters
        '''
        filter_ = Q(**self.get_regenerate_log_filter())

        try:
            regen_obj = RegenerationLog.objects.get(filter_)
        except RegenerationLog.DoesNotExist:
            regen_obj = None

        self.regen_obj = regen_obj

        return regen_obj

    def get_object(self):
        '''
        Entrypoint function for inheriting classes to get the object.
        
        Regenerates if marked.
        '''
        regen_obj = self.get_regeneration_log_object()
        obj = self.get_object_hook()

        if regen_obj:
            RegenerableView.logger.debug("---------------------Regeneration Object Found")
            return self.regeneration_hook(obj)

        #No Regeneration is required so just return the obj
        return obj

    def request_end_hook(self):

        if getattr(self , "regen_obj"):
            self.regen_obj.toggleStatus()
        return


class TestRegenerableView(RegenerableView):

    type = "diet"

    def get_object_hook(self):
        return model.objects.last()

    def get_regenerate_log_filter(self):
        '''
        Customer , Year , Week , Type , regenerated
        '''
        return  Q(customer = customer) & Q(year = year) & Q(week = week) & Q(type = self.diet) & Q(regenerated = False)
