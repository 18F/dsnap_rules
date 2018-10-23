import copy
from unittest.mock import patch

import pytest

from new_rules.app import app


GOOD_PAYLOAD = {
    "is_head_of_household": True,
    "is_authorized_representative": False,
    "has_lost_or_inaccessible_income": False,
    "has_inaccessible_liquid_resources": True,
    "incurred_deductible_disaster_expenses": False,
    "total_take_home_income": 200,
    "accessible_liquid_resources": 0,
    "deductible_disaster_expenses": 0,
    "state_or_territory": "CA",
    "size_of_household": 4
}


@pytest.fixture
def client():
    client = app.test_client()
    yield client


def test_missing_required_field(client):
    payload = copy.deepcopy(GOOD_PAYLOAD)
    del payload["is_head_of_household"]

    response = client.post('/', json=payload)

    assert response.status_code == 400
    assert response.json["message"] == (
        "'is_head_of_household' is a required property")


def test_invalid_field_format(client):
    payload = copy.deepcopy(GOOD_PAYLOAD)
    payload["size_of_household"] = "2"

    response = client.post('/', json=payload)

    assert response.status_code == 400
    assert response.json["message"] == (
        "'2' is not of type 'integer'")


@patch('new_rules.dsnap.dgi_calculator.get_dgi_calculator')
def test_basic_eligible_payload(get_dgi_calculator_mock, client):
    LIMIT = 500
    ALLOTMENT = 100
    get_dgi_calculator_mock.return_value.get_limit.return_value = LIMIT
    get_dgi_calculator_mock.return_value.get_allotment.return_value = ALLOTMENT
    payload = copy.deepcopy(GOOD_PAYLOAD)

    response = client.post('/', json=payload)

    assert response.status_code == 200
    assert response.json == {
        "eligible": True,
        "findings": [
            "Either head of household or authorized representative",
            "Experienced disaster-related adverse effects",
            f"Gross income {payload['total_take_home_income']} within "
            f"limit of {LIMIT}"
        ],
        "metrics": {"allotment": ALLOTMENT}
    }


@patch('new_rules.dsnap.dgi_calculator.get_dgi_calculator')
def test_basic_ineligible_payload(get_dgi_calculator_mock, client):
    LIMIT = 500
    ALLOTMENT = 100
    get_dgi_calculator_mock.return_value.get_limit.return_value = LIMIT
    get_dgi_calculator_mock.return_value.get_allotment.return_value = ALLOTMENT
    payload = copy.deepcopy(GOOD_PAYLOAD)
    payload["is_head_of_household"] = False

    response = client.post('/', json=payload)

    assert response.status_code == 200
    assert response.json == {
        "eligible": False,
        "findings": [
            "Neither head of household nor authorized representative",
            "Experienced disaster-related adverse effects",
            f"Gross income {payload['total_take_home_income']} within "
            f"limit of {LIMIT}"
        ],
        "metrics": {"allotment": ALLOTMENT}
    }
    assert not response.json["eligible"]
