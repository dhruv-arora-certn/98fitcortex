import functools
import datetime
import types

from django.utils import timezone
from django.core.cache import cache

KEY_TEMPLATE = "%d_%s" #Template for cache "userid_key"

modules = types.SimpleNamespace()

modules.SLEEP_LOGS = "sleep_logs"
modules.SLEEP_AGGREGATE = "sleep_aggregate"
modules.SLEEP = "sleep"
modules.ACTIVITY_LOGS = "activity_logs"
modules.ACTIVITY_AGGREGATE = "activity_aggregate"
modules.ACTIVITY = "activity"
modules.DIET_DASHBOARD_STRING = "diet_dashboard_string"
modules.DIET_PLAN = "diet_plan"
modules.DIET = "diet"

@functools.lru_cache()
def get_cache_key(user, module):
    '''
    Get Cache key for the user for the module specified
    '''
    data = {
        modules.SLEEP_LOGS : get_sleep_logs_cache_key,
        modules.SLEEP_AGGREGATE : get_sleep_aggregate_cache_key,
        modules.ACTIVITY_LOGS : get_activity_logs_cache_key,
        modules.ACTIVITY_AGGREGATE : get_activity_aggregate_cache_key,
        modules.DIET_DASHBOARD_STRING : get_diet_dashboard_string_cache_key,
        modules.SLEEP : get_sleep_cache_keys,
        modules.DIET_PLAN : get_dietplan_cache_key,
        modules.DIET : get_diet_cache_keys
    } 
    return data.get(module)(user)

@functools.lru_cache()
def get_sleep_logs_cache_key(user):
    return KEY_TEMPLATE%(
        user.id, modules.SLEEP_LOGS
    )

@functools.lru_cache()
def get_sleep_aggregate_cache_key(user):
    return KEY_TEMPLATE%(
        user.id, modules.SLEEP_AGGREGATE
    )

@functools.lru_cache()
def get_activity_logs_cache_key(user):
    return KEY_TEMPLATE%(
        user.id, modules.ACTIVITY_LOGS
    )

@functools.lru_cache()
def get_activity_aggregate_cache_key(user):
    return KEY_TEMPLATE%(
        user.id, modules.ACTIVITY_AGGREGATE
    )

@functools.lru_cache()
def get_diet_dashboard_string_cache_key(user):
    return KEY_TEMPLATE %(
        user.id, modules.DIET_DASHBOARD_STRING
    )

@functools.lru_cache()
def get_dietplan_cache_key(user):
    return KEY_TEMPLATE%(
        user.id, modules.DIET_PLAN
    )

@functools.lru_cache()
def get_sleep_cache_keys(user):
    '''
    Return all the cache keys for a user belonging to a particular module
    '''
    return [
        KEY_TEMPLATE%(user.id, e) for e in [modules.SLEEP_LOGS, modules.SLEEP_AGGREGATE]
    ]

@functools.lru_cache()
def get_diet_cache_keys(user):
    '''
    Return all the keys for a user belonging to diet module
    '''
    return [
        KEY_TEMPLATE%(user.id, e) for e in [
            modules.DIET_DASHBOARD_STRING, modules.DIET_PLAN
        ]
    ]

def get_time_to_midnight(time = None):
    '''
    Return the seconds to coming midnight
    '''
    if not time:
        time = datetime.datetime.now( tz = timezone.get_current_timezone())

    mid = time.replace(hour = 0, minute = 0, second = 0)

    return 86400 - (time - mid).seconds


def invalidate_cache(user, module):
    '''
    Invalidate Caches of a module for a user 
    '''
    key = get_cache_key(user, module)

    if isinstance(key, list):
        return cache.delete_many(key)
    elif isinstance(key, str):
        return cache.delete(key)
    return
