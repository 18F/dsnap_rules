import copy
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from . import factories
from dsnap_rules.dsnap_rules import (AdverseEffectRule, AuthorizedRule,
                                     ConflictingUSDAProgramRule,
                                     FoodPurchaseRule, ResidencyRule,
                                     SNAPSupplementalBenefitsRule)

GOOD_PAYLOAD = {
    "disaster_request_no": "DR-1",
    "disaster_expenses": {
        "food_loss": 0,
    },
    "is_head_of_household": True,
    "is_authorized_representative": False,
    "has_lost_or_inaccessible_income": False,
    "has_inaccessible_liquid_resources": True,
    "purchased_or_plans_to_purchase_food": True,
    "resided_in_disaster_area_at_disaster_time": True,
    "worked_in_disaster_area_at_disaster_time": False,
    "total_take_home_income": 200,
    "accessible_liquid_resources": 0,
    "size_of_household": 4,
    "receives_FDPIR_benefits": False,
    "receives_TEFAP_food_distribution": False,
    "receives_SNAP_benefits": False,
}


def test_missing_required_field(client):
    payload = copy.deepcopy(GOOD_PAYLOAD)
    del payload["is_head_of_household"]

    response = client.post('/', data=payload, content_type="application/json")

    assert response.status_code == 400
    assert response.json() == {
        "message": ["'is_head_of_household' is a required property"]
    }


def test_invalid_field_format(client):
    payload = copy.deepcopy(GOOD_PAYLOAD)
    payload["size_of_household"] = "2"

    response = client.post('/', data=payload, content_type="application/json")

    assert response.status_code == 400
    assert response.json() == {
        "message": ["'2' is not of type 'integer'"]
    }


@pytest.mark.django_db
def test_invalid_disaster(client):
    payload = copy.deepcopy(GOOD_PAYLOAD)
    response = client.post('/', data=payload, content_type="application/json")

    assert response.status_code == 404
    assert response.json() == {
        "message": "Disaster {} not found".format(
            payload["disaster_request_no"])
    }


@pytest.mark.django_db
@patch('dsnap_rules.income_allotment_calculator.get_calculator')
def test_valid_disaster(get_calculator_mock, client):
    LIMIT = 500
    ALLOTMENT = 100
    get_calculator_mock.return_value.get_limit.return_value = LIMIT
    get_calculator_mock.return_value.get_allotment.return_value = ALLOTMENT
    payload = copy.deepcopy(GOOD_PAYLOAD)
    disaster = factories.DisasterFactory(
        disaster_request_no=payload["disaster_request_no"],
        residency_required=True,
        uses_DSED=False,
        allows_food_loss_alone=True,
    )
    response = client.post('/', data=payload, content_type="application/json")

    assert response.status_code == 200
    assert response.json() == {
        "eligible": True,
        "findings": [
            {
                "rule": "AuthorizedRule",
                "succeeded": True,
                "text": AuthorizedRule.success_finding
            },
            {
                "rule": "AdverseEffectRule",
                "succeeded": True,
                "text": AdverseEffectRule.success_finding
            },
            {
                "rule": "FoodPurchaseRule",
                "succeeded": True,
                "text": FoodPurchaseRule.success_finding
            },
            {
                "rule": "ResidencyRule",
                "succeeded": True,
                "text": ResidencyRule.resided_finding
            },
            {
                "rule": "ConflictingUSDAProgramRule",
                "succeeded": True,
                "text": ConflictingUSDAProgramRule.success_finding
            },
            {
                "rule": "SNAPSupplementalBenefitsRule",
                "succeeded": True,
                "text": SNAPSupplementalBenefitsRule.success_finding
            },
            {
                "rule": "IncomeAndResourceRule",
                "succeeded": True,
                "text": f"Gross income {payload['total_take_home_income']} "
                        f"within limit of {LIMIT}"
            },
        ],
        "metrics": {"allotment": ALLOTMENT},
        "state": disaster.state.abbreviation
    }


@pytest.mark.django_db
@patch('dsnap_rules.income_allotment_calculator.get_calculator')
def test_basic_ineligible_payload(get_calculator_mock, client):
    LIMIT = 500
    ALLOTMENT = 100
    get_calculator_mock.return_value.get_limit.return_value = LIMIT
    get_calculator_mock.return_value.get_allotment.return_value = ALLOTMENT
    payload = copy.deepcopy(GOOD_PAYLOAD)
    payload["is_head_of_household"] = False
    disaster = factories.DisasterFactory(
        disaster_request_no=payload["disaster_request_no"],
        residency_required=True,
        uses_DSED=False,
        allows_food_loss_alone=True,
    )
    response = client.post('/', data=payload, content_type="application/json")

    assert response.status_code == 200
    assert response.json() == {
        "eligible": False,
        "findings": [
            {
                "rule": "AuthorizedRule",
                "succeeded": False,
                "text": AuthorizedRule.failure_finding
            },
            {
                "rule": "AdverseEffectRule",
                "succeeded": True,
                "text": AdverseEffectRule.success_finding
            },
            {
                "rule": "FoodPurchaseRule",
                "succeeded": True,
                "text": FoodPurchaseRule.success_finding
            },
            {
                "rule": "ResidencyRule",
                "succeeded": True,
                "text": ResidencyRule.resided_finding
            },
            {
                "rule": "ConflictingUSDAProgramRule",
                "succeeded": True,
                "text": ConflictingUSDAProgramRule.success_finding
            },
            {
                "rule": "SNAPSupplementalBenefitsRule",
                "succeeded": True,
                "text": SNAPSupplementalBenefitsRule.success_finding
            },
            {
                "rule": "IncomeAndResourceRule",
                "succeeded": True,
                "text": f"Gross income {payload['total_take_home_income']} "
                        f"within limit of {LIMIT}"
            },
        ],
        "metrics": {"allotment": ALLOTMENT},
        "state": disaster.state.abbreviation
    }


@pytest.mark.django_db
def test_get_disasters_with_single_application_periods(client):
    today = timezone.localdate()

    active_period = factories.ApplicationPeriodFactory.build(
        registration_begin_date=today - timedelta(days=1),
        registration_end_date=today + timedelta(days=5),
    )
    disaster_with_active_period = factories.DisasterFactory()
    disaster_with_active_period.application_periods.add(
        active_period,
        bulk=False
    )

    past_period = factories.ApplicationPeriodFactory.build(
        registration_begin_date=today - timedelta(days=10),
        registration_end_date=today - timedelta(days=5),
    )
    disaster_with_past_active_period = factories.DisasterFactory()
    disaster_with_past_active_period.application_periods.add(
        past_period,
        bulk=False
    )

    future_period = factories.ApplicationPeriodFactory.build(
        registration_begin_date=today + timedelta(days=5),
        registration_end_date=today + timedelta(days=10),
    )
    disaster_with_future_active_period = factories.DisasterFactory()
    disaster_with_future_active_period.application_periods.add(
        future_period,
        bulk=False
    )

    response = client.get('/disasters')

    assert response.status_code == 200
    returned_titles = [d['title'] for d in response.json()]
    assert disaster_with_active_period.title in returned_titles
    assert disaster_with_past_active_period.title not in returned_titles
    assert disaster_with_future_active_period.title not in returned_titles


@pytest.mark.django_db
def test_get_disasters_with_multiple_application_periods(client):
    today = timezone.localdate()

    active_period1 = factories.ApplicationPeriodFactory.build(
        registration_begin_date=today - timedelta(days=5),
        registration_end_date=today + timedelta(days=1),
    )
    active_period2 = factories.ApplicationPeriodFactory.build(
        registration_begin_date=today - timedelta(days=1),
        registration_end_date=today + timedelta(days=5),
    )
    disaster_with_2_active_periods = factories.DisasterFactory()
    disaster_with_2_active_periods.application_periods.add(
        active_period1,
        active_period2,
        bulk=False
    )

    active_period = factories.ApplicationPeriodFactory.build(
        registration_begin_date=today - timedelta(days=5),
        registration_end_date=today + timedelta(days=5),
    )
    future_period = factories.ApplicationPeriodFactory.build(
        registration_begin_date=today + timedelta(days=5),
        registration_end_date=today + timedelta(days=10),
    )
    disaster_with_1_active_1_future_period = factories.DisasterFactory()
    disaster_with_1_active_1_future_period.application_periods.add(
        active_period,
        future_period,
        bulk=False
    )

    response = client.get('/disasters')

    assert response.status_code == 200
    assert len(response.json()) == 2
    returned_titles = [d['title'] for d in response.json()]
    assert disaster_with_2_active_periods.title in returned_titles
    assert disaster_with_1_active_1_future_period.title in returned_titles
