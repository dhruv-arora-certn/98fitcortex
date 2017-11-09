import pytest

from django.core.cache import cache

@pytest.fixture
def workout():
	return cache.get("workout_8_45_1")
