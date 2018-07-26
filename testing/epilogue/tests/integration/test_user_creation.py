import pytest

from epilogue import models

from django.urls import reverse


@pytest.fixture
def user_creation_data():
    return {
        "first_name" : "Shikhar"
    }

@pytest.fixture
def user():
    print(models.Customer.objects.count())
    return models.Customer.objects.first()

@pytest.mark.django_db
def test_a_respond_201_when_user_onboards_only_with_name(client, user_creation_data):
    print("Executing test 1 *****")
    response = client.post(
        reverse("user"), user_creation_data
    )
    assert response.status_code == 201

@pytest.mark.django_db
def a_test_b_respond_update_when_user_adds_gender(client,user):
    print("Executing test 2")
    response = client.post(
        reverse("user-entry", kwargs = {"pk":user.id}),
        {
            "gender": "male"
        },
        AUTHORIZATION = "Token %d"%user.auth_token.key
    )
    assert response.status_code == 200, "Something Went wrong"


