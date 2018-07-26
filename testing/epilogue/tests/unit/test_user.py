import pytest

from epilogue import models

from django.core.management import call_command


@pytest.fixture
def myfixture(django_db_blocker):
    print("Calling Command")
    with django_db_blocker.unblock():
        call_command("load_data","foods.json")


