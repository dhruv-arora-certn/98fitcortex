from django.apps import apps

import logging

apps_to_migrate = [
    "epilogue",
    "workout",
    "authentication",
    "analytics",
    "regeneration"
]


logger = logging.getLogger("migration_script")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("migration.log")

logger.addHandler(handler)

def log_written_objs(objs):
    for e in objs:
        logger.debug(str(e))



def get_app_models(app):
    models = apps.get_app_config(app).get_models()
    return models

def transfer(app , start= 0 ):
    models = get_app_models(app)
    if not start:
        start = 0

    for model in models:
        items = model.objects.using('main').all()
        start = 0
        count = items.count()

        for i in range(start , count , 100):
            items_to_transfer = items[i:i+100]
            created = model.objects.bulk_create(items_to_transfer)
            log_written_objs(created)

    return



