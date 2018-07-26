import pytest 
from unittest import mock
import functools


@pytest.fixture
def client():
    from django.test.client import Client

    return Client()

@pytest.fixture
def user_creation_data():
    return {
        "first_name" : "Shikhar"
    }

