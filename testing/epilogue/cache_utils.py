import functools
import datetime
import types

from django.utils import timezone

KEY_TEMPLATE = "%d_%s" #Template for cache "userid_key"

modules = types.SimpleNamespace()

modules.SLEEP_LOGS = "sleep_logs"
modules.SLEEP_AGGREGATE = "sleep_aggregate"
modules.ACTIVITY_LOGS = "activity_logs"
modules.ACTIVITY_AGGREGATE = "activity_aggregate"

@functools.lru_cache()
def get_cache_key(user, module):
    '''
    Get Cache key for the user for the module specified
    '''
    if module == "sleep_logs":
        return get_sleep_logs_cache_key(user)
    elif module == "sleep_aggregate":
        return get_sleep_aggregate_cache_key(user)
    elif module == "activity_logs":
        return get_activity_logs_cache_key(user) 
    elif module == "activity_aggregate":
        return get_activity_aggregate_cache_key(user)

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

def get_time_to_midnight(time = None):
    '''
    Return the seconds to coming midnight
    '''
    if not time:
        time = datetime.datetime.now( tz = timezone.get_current_timezone())

    mid = time.replace(hour = 0, minute = 0, second = 0)

    return 86400 - (time - mid).seconds
