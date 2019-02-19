from unittest.mock import patch

import pytest

from dsnap_rules.dsnap_rules import (AdverseEffectRule, AuthorizedRule,
                                     IncomeAndResourceRule, ResidencyRule)
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

    actual_result = AuthorizedRule().execute(payload, disaster=None)
    assert actual_result == Result(successful, findings=[{
                "rule": "AuthorizedRule",
                "succeeded": successful,
                "text": finding
            }])


@pytest.mark.parametrize(
    "has_lost_or_inaccessible_income, has_inaccessible_liquid_resources,"
    "incurred_deductible_disaster_expenses, successful, finding",
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
def test_adverse_effect_rule(
        has_lost_or_inaccessible_income, has_inaccessible_liquid_resources,
        incurred_deductible_disaster_expenses, successful, finding):

    payload = {
        "has_lost_or_inaccessible_income": has_lost_or_inaccessible_income,
        "has_inaccessible_liquid_resources": has_inaccessible_liquid_resources,
        "incurred_deductible_disaster_expenses":
            incurred_deductible_disaster_expenses,
    }

    actual_result = AdverseEffectRule().execute(payload, disaster=None)
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
        (True, True, False, True, ResidencyRule.resided_finding),
        (True, True, True, True, ResidencyRule.resided_finding),
        (True, False, False, True, ResidencyRule.resided_finding),
        (True, False, True, True, ResidencyRule.resided_finding),
        (False, True, False, True, ResidencyRule.worked_eligible_finding),
        (False, True, True, False, ResidencyRule.worked_ineligible_finding),
        (False, False, False, False, ResidencyRule.failure_finding),
        (False, False, True, False, ResidencyRule.failure_finding),
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
    disaster = Disaster(residency_required=residency_required)

    actual_result = ResidencyRule().execute(payload, disaster=disaster)
    assert actual_result == Result(successful, findings=[{
                "rule": "ResidencyRule",
                "succeeded": successful,
                "text": finding
            }])


def test_the_and_rule():
    payload = {
        "is_head_of_household": True,
        "is_authorized_representative": False,
        "has_lost_or_inaccessible_income": False,
        "has_inaccessible_liquid_resources": True,
        "incurred_deductible_disaster_expenses": False,
    }
    assert_result(
        And(AuthorizedRule(), AdverseEffectRule()),
        payload,
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

    payload["has_inaccessible_liquid_resources"] = False
    assert_result(
        And(AuthorizedRule(), AdverseEffectRule()),
        payload,
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

    payload["is_head_of_household"] = False
    payload["has_inaccessible_liquid_resources"] = True
    assert_result(
        And(AuthorizedRule(), AdverseEffectRule()),
        payload,
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


@patch('dsnap_rules.income_allotment_calculator.get_calculator')
def test_income_and_resource(get_calculator_mock):
    LIMIT = 500
    ALLOTMENT = 100
    get_calculator_mock.return_value.get_limit.return_value = LIMIT
    get_calculator_mock.return_value.get_allotment.return_value = ALLOTMENT

    TOTAL_TAKE_HOME_INCOME = 200
    ACCESSIBLE_LIQUID_RESOURCES = 300
    DEDUCTIBLE_DISASTER_EXPENSES = 50

    VERY_LARGE_TAKE_HOME_INCOME = 2 * LIMIT

    payload = {
        "total_take_home_income": TOTAL_TAKE_HOME_INCOME,
        "accessible_liquid_resources": ACCESSIBLE_LIQUID_RESOURCES,
        "deductible_disaster_expenses": DEDUCTIBLE_DISASTER_EXPENSES,
        "size_of_household": 4
    }
    gross_income = (TOTAL_TAKE_HOME_INCOME + ACCESSIBLE_LIQUID_RESOURCES
                    - DEDUCTIBLE_DISASTER_EXPENSES)
    assert_result(
        IncomeAndResourceRule(),
        payload,
        Result(True,
               findings=[{
                "rule": "IncomeAndResourceRule",
                "succeeded": True,
                "text": f"Gross income {gross_income} within limit of {LIMIT}"
                }],
               metrics={"allotment": ALLOTMENT})
    )

    payload["total_take_home_income"] = VERY_LARGE_TAKE_HOME_INCOME
    gross_income = (VERY_LARGE_TAKE_HOME_INCOME + ACCESSIBLE_LIQUID_RESOURCES
                    - DEDUCTIBLE_DISASTER_EXPENSES)
    assert_result(
        IncomeAndResourceRule(),
        payload,
        Result(False,
               findings=[{
                "rule": "IncomeAndResourceRule",
                "succeeded": False,
                "text": f"Gross income {gross_income} exceeds limit of {LIMIT}"
                }])
    )


@patch('dsnap_rules.income_allotment_calculator.get_calculator')
def test_DSED_calculation(get_calculator_mock):
    LIMIT = 500
    ALLOTMENT = 100
    get_calculator_mock.return_value.get_limit.return_value = LIMIT
    get_calculator_mock.return_value.get_allotment.return_value = ALLOTMENT

    TOTAL_TAKE_HOME_INCOME = 100
    ACCESSIBLE_LIQUID_RESOURCES = 450
    DEDUCTIBLE_DISASTER_EXPENSES = 50

    payload = {
        "total_take_home_income": TOTAL_TAKE_HOME_INCOME,
        "accessible_liquid_resources": ACCESSIBLE_LIQUID_RESOURCES,
        "deductible_disaster_expenses": DEDUCTIBLE_DISASTER_EXPENSES,
        "size_of_household": 4
    }
    disaster = Disaster(uses_DSED=True)
    # Don't subtract disaster expenses when DSED in use
    gross_income = (TOTAL_TAKE_HOME_INCOME + ACCESSIBLE_LIQUID_RESOURCES)

    assert_result(
        IncomeAndResourceRule(),
        payload,
        Result(False,
               findings=[{
                "rule": "IncomeAndResourceRule",
                "succeeded": False,
                "text": f"Gross income {gross_income} exceeds limit of {LIMIT}"
                }]),
        disaster=disaster
    )


def assert_result(rule, payload, expected_result, disaster=None):
    if disaster is None:
        disaster = Disaster()
    actual_result = rule.execute(payload, disaster=disaster)
    assert actual_result == expected_result
