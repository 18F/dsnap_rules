from unittest.mock import patch

import pytest

from dsnap_rules.dsnap_application import DSNAPApplication
from dsnap_rules.dsnap_rules import (
    AdverseEffectRule,
    AuthorizedRule,
    DisasterAreaResidencyRule,
    IncomeAndResourceRule,
)
from dsnap_rules.models import Disaster
from dsnap_rules.rules import And, Result


@pytest.mark.parametrize(
    "is_head_of_household, is_authorized_representative, successful, finding",
    [
        (True, True, True, AuthorizedRule.success_finding),
        (True, False, True, AuthorizedRule.success_finding),
        (False, True, True, AuthorizedRule.success_finding),
        (False, False, False, AuthorizedRule.failure_finding),
    ])
def test_authorized_rule(is_head_of_household, is_authorized_representative,
                         successful, finding):

    payload = {
        "is_head_of_household": is_head_of_household,
        "is_authorized_representative": is_authorized_representative,
    }
    application = DSNAPApplication(payload)

    actual_result = AuthorizedRule().execute(application, disaster=None)
    assert actual_result == Result(successful, findings=[{
                "rule": "AuthorizedRule",
                "succeeded": successful,
                "text": finding
            }])


@pytest.mark.parametrize(
    "has_lost_or_inaccessible_income, has_inaccessible_liquid_resources,"
    "has_disaster_expenses, successful, finding",
    [
        (True, True, True, True, AdverseEffectRule.success_finding),
        (True, True, False, True, AdverseEffectRule.success_finding),
        (True, False, True, True, AdverseEffectRule.success_finding),
        (True, False, False, True, AdverseEffectRule.success_finding),
        (False, True, True, True, AdverseEffectRule.success_finding),
        (False, True, False, True, AdverseEffectRule.success_finding),
        (False, False, True, True, AdverseEffectRule.success_finding),
        (False, False, False, False, AdverseEffectRule.failure_finding),
    ])
def test_adverse_effect_rule_independent_of_food_loss_alone_setting(
        has_lost_or_inaccessible_income, has_inaccessible_liquid_resources,
        has_disaster_expenses, successful, finding):
    HOME_REPAIR_EXPENSES = 200  # Test food loss alone rules separately
    payload = {
        "has_lost_or_inaccessible_income": has_lost_or_inaccessible_income,
        "has_inaccessible_liquid_resources": has_inaccessible_liquid_resources,
        "disaster_expenses": {
            "home_or_business_repairs":
                HOME_REPAIR_EXPENSES if has_disaster_expenses else 0
        }
    }
    application = DSNAPApplication(payload)
    disaster = Disaster(uses_DSED=False, allows_food_loss_alone=True)

    actual_result = AdverseEffectRule().execute(application, disaster=disaster)
    assert actual_result == Result(successful, findings=[{
                "rule": "AdverseEffectRule",
                "succeeded": successful,
                "text": finding
            }])


@pytest.mark.parametrize(
    "food_loss_alone, food_loss,"
    "non_food_loss, successful, finding",
    [
        (True, 100, 0, True, AdverseEffectRule.success_finding),
        (True, 0, 100, True, AdverseEffectRule.success_finding),
        (False, 100, 0, False, AdverseEffectRule.failure_finding),
        (False, 0, 100, True, AdverseEffectRule.success_finding),
    ])
def test_adverse_effect_rule_with_food_loss_alone_setting(
        food_loss_alone, food_loss,
        non_food_loss, successful, finding):
    payload = {
        "has_lost_or_inaccessible_income": False,
        "has_inaccessible_liquid_resources": False,
        "disaster_expenses": {
            "food_loss": food_loss,
            "home_or_business_repairs": non_food_loss
        }
    }
    application = DSNAPApplication(payload)
    disaster = Disaster(uses_DSED=False,
                        allows_food_loss_alone=food_loss_alone)

    actual_result = AdverseEffectRule().execute(application, disaster=disaster)
    assert actual_result == Result(successful, findings=[{
                "rule": "AdverseEffectRule",
                "succeeded": successful,
                "text": finding
            }])


@pytest.mark.parametrize(
    "resided_in_disaster_area_at_disaster_time,"
    "worked_in_disaster_area_at_disaster_time,"
    "residency_required,"
    "successful, finding",
    [
        (True, True, False, True, DisasterAreaResidencyRule.resided_finding),
        (True, True, True, True, DisasterAreaResidencyRule.resided_finding),
        (True, False, False, True, DisasterAreaResidencyRule.resided_finding),
        (True, False, True, True, DisasterAreaResidencyRule.resided_finding),
        (False, True, False, True,
            DisasterAreaResidencyRule.worked_eligible_finding),
        (False, True, True, False,
            DisasterAreaResidencyRule.worked_ineligible_finding),
        (False, False, False, False,
            DisasterAreaResidencyRule.failure_finding),
        (False, False, True, False,
            DisasterAreaResidencyRule.failure_finding),
    ])
def test_residency_rule(
        resided_in_disaster_area_at_disaster_time,
        worked_in_disaster_area_at_disaster_time,
        residency_required,
        successful, finding):

    payload = {
        "resided_in_disaster_area_at_disaster_time":
            resided_in_disaster_area_at_disaster_time,
        "worked_in_disaster_area_at_disaster_time":
            worked_in_disaster_area_at_disaster_time
    }
    application = DSNAPApplication(payload)
    disaster = Disaster(residency_required=residency_required)

    actual_result = DisasterAreaResidencyRule().execute(
        application, disaster=disaster)
    assert actual_result == Result(successful, findings=[{
                "rule": "DisasterAreaResidencyRule",
                "succeeded": successful,
                "text": finding
            }])


def test_the_and_rule():
    payload = {
        "is_head_of_household": True,
        "is_authorized_representative": False,
        "has_lost_or_inaccessible_income": False,
        "has_inaccessible_liquid_resources": True,
        "disaster_expenses": {}
    }
    application = DSNAPApplication(payload)
    assert_result(
        And(AuthorizedRule(), AdverseEffectRule()),
        application,
        Result(True,
               findings=[{
                "rule": "AuthorizedRule",
                "succeeded": True,
                "text": AuthorizedRule.success_finding,
                }, {
                "rule": "AdverseEffectRule",
                "succeeded": True,
                "text": AdverseEffectRule.success_finding
                }])
    )

    application.has_inaccessible_liquid_resources = False
    assert_result(
        And(AuthorizedRule(), AdverseEffectRule()),
        application,
        Result(False,
               findings=[{
                "rule": "AuthorizedRule",
                "succeeded": True,
                "text": AuthorizedRule.success_finding
                }, {
                "rule": "AdverseEffectRule",
                "succeeded": False,
                "text": AdverseEffectRule.failure_finding
                }])
    )

    application.is_head_of_household = False
    application.has_inaccessible_liquid_resources = True
    assert_result(
        And(AuthorizedRule(), AdverseEffectRule()),
        application,
        Result(False,
               findings=[{
                "rule": "AuthorizedRule",
                "succeeded": False,
                "text": AuthorizedRule.failure_finding,
                }, {
                "rule": "AdverseEffectRule",
                "succeeded": True,
                "text": AdverseEffectRule.success_finding
                }])
    )


@pytest.mark.parametrize(
    "income, allows_food_loss_alone, food_loss, non_food_loss, limit,"
    "successful, finding_text",
    [
        (   # Only food loss; food loss alone allowed
            530, True, 50, 0, 500,
            True, "Disaster Gross Income 480 within limit of 500"
        ),
        (   # Only non-food losses; food loss alone allowed
            530, True, 0, 50, 500,
            True, "Disaster Gross Income 480 within limit of 500"
        ),
        (   # Only food loss; food loss alone not allowed
            530, False, 50, 0, 500,
            False, "Disaster Gross Income 530 exceeds limit of 500"
        ),
        (   # Only non-food losses; food loss alone not allowed
            530, False, 0, 50, 500,
            True, "Disaster Gross Income 480 within limit of 500"
        ),
        (   # Food loss + non-food losses; food loss alone allowed, both needed
            # to meet limit
            530, True, 25, 25, 500,
            True, "Disaster Gross Income 480 within limit of 500"
        ),
        (   # Food loss + non-food losses; food loss alone not allowed, both
            # needed to meet limit
            530, False, 25, 25, 500,
            True, "Disaster Gross Income 480 within limit of 500"
        ),
        (   # Food loss + non-food losses; food loss alone allowed, income too
            # high
            1530, True, 25, 25, 500,
            False, "Disaster Gross Income 1480 exceeds limit of 500"
        ),
    ])
@patch('dsnap_rules.income_allotment_calculator.get_calculator')
def test_income_and_resource_rule(
        get_calculator_mock,
        income, allows_food_loss_alone, food_loss, non_food_loss, limit,
        successful, finding_text):
    ALLOTMENT = 100
    get_calculator_mock.return_value.get_limit.return_value = limit
    get_calculator_mock.return_value.get_allotment.return_value = ALLOTMENT

    payload = {
        "total_take_home_income": income,
        "accessible_liquid_resources": 0,
        "disaster_expenses": {
            "food_loss": food_loss,
            "home_or_business_repairs": non_food_loss,
        },
        "size_of_household": 4
    }
    application = DSNAPApplication(payload)
    disaster = Disaster(uses_DSED=False,
                        allows_food_loss_alone=allows_food_loss_alone)
    result = IncomeAndResourceRule().execute(application, disaster=disaster)
    assert result.successful is successful
    assert finding_text == result.findings[0]["text"]


@patch('dsnap_rules.income_allotment_calculator.get_calculator')
def test_DSED_calculation(get_calculator_mock):
    LIMIT = 500
    ALLOTMENT = 100
    get_calculator_mock.return_value.get_limit.return_value = LIMIT
    get_calculator_mock.return_value.get_allotment.return_value = ALLOTMENT

    TOTAL_TAKE_HOME_INCOME = 100
    ACCESSIBLE_LIQUID_RESOURCES = 450
    HOME_OR_BUSINESS_REPAIRS = 50

    payload = {
        "total_take_home_income": TOTAL_TAKE_HOME_INCOME,
        "accessible_liquid_resources": ACCESSIBLE_LIQUID_RESOURCES,
        "disaster_expenses": {
            "home_or_business_repairs": HOME_OR_BUSINESS_REPAIRS,
        },
        "size_of_household": 4
    }
    application = DSNAPApplication(payload)
    disaster = Disaster(uses_DSED=True)
    # Don't subtract disaster expenses when DSED in use
    gross_income = (TOTAL_TAKE_HOME_INCOME + ACCESSIBLE_LIQUID_RESOURCES)

    assert_result(
        IncomeAndResourceRule(),
        application,
        Result(False,
               findings=[{
                "rule": "IncomeAndResourceRule",
                "succeeded": False,
                "text": f"Disaster Gross Income {gross_income} exceeds "
                        f"limit of {LIMIT}"
                }]),
        disaster=disaster
    )


def assert_result(rule, application, expected_result, disaster=None):
    if disaster is None:
        disaster = Disaster()
    actual_result = rule.execute(application, disaster=disaster)
    assert actual_result == expected_result
