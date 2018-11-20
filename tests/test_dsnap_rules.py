from unittest.mock import patch, Mock

import pytest

from dsnap_rules.config import get_config, Config
from dsnap_rules.rules import And, Result
from dsnap_rules.dsnap_rules import (
    AdverseEffectRule,
    AuthorizedRule,
    IncomeAndResourceRule,
    ResidencyRule,
)


@pytest.mark.parametrize(
    "is_head_of_household, is_authorized_representative, successful, findings",
    [
        (True, True, True, AuthorizedRule.success_finding),
        (True, False, True, AuthorizedRule.success_finding),
        (False, True, True, AuthorizedRule.success_finding),
        (False, False, False, AuthorizedRule.failure_finding),
    ])
def test_authorized_rule(is_head_of_household, is_authorized_representative,
                         successful, findings):

    payload = {
        "is_head_of_household": is_head_of_household,
        "is_authorized_representative": is_authorized_representative,
    }

    actual_result = AuthorizedRule().execute(payload, config=None)
    assert actual_result == Result(successful, findings=[findings])


@pytest.mark.parametrize(
    "has_lost_or_inaccessible_income, has_inaccessible_liquid_resources,"
    "incurred_deductible_disaster_expenses, successful, findings",
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
        incurred_deductible_disaster_expenses, successful, findings):

    payload = {
        "has_lost_or_inaccessible_income": has_lost_or_inaccessible_income,
        "has_inaccessible_liquid_resources": has_inaccessible_liquid_resources,
        "incurred_deductible_disaster_expenses":
            incurred_deductible_disaster_expenses,
    }

    actual_result = AdverseEffectRule().execute(payload, config=None)
    assert actual_result == Result(successful, findings=[findings])


@pytest.mark.parametrize(
    "resided_in_disaster_area_at_disaster_time,"
    "worked_in_disaster_area_at_disaster_time,"
    "worked_in_disaster_area_is_dsnap_eligible,"
    "successful, findings",
    [
        (True, True, True, True, ResidencyRule.success_finding),
        (True, True, False, True, ResidencyRule.success_finding),
        (True, False, True, True, ResidencyRule.success_finding),
        (True, False, False, True, ResidencyRule.success_finding),
        (False, True, True, True, ResidencyRule.success_finding),
        (False, True, False, False, ResidencyRule.failure_finding),
        (False, False, True, False, ResidencyRule.failure_finding),
        (False, False, False, False, ResidencyRule.failure_finding),
    ])
def test_residency_rule(
        resided_in_disaster_area_at_disaster_time,
        worked_in_disaster_area_at_disaster_time,
        worked_in_disaster_area_is_dsnap_eligible,
        successful, findings):

    payload = {
        "resided_in_disaster_area_at_disaster_time":
            resided_in_disaster_area_at_disaster_time,
        "worked_in_disaster_area_at_disaster_time":
            worked_in_disaster_area_at_disaster_time
    }
    config = Config(
        worked_in_disaster_area_is_dsnap_eligible=
            worked_in_disaster_area_is_dsnap_eligible)

    actual_result = ResidencyRule().execute(payload, config=config)
    assert actual_result == Result(successful, findings=[findings])


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
               findings=[
                   "Either head of household or authorized representative",
                   "Experienced disaster-related adverse effects"])
    )

    payload["has_inaccessible_liquid_resources"] = False
    assert_result(
        And(AuthorizedRule(), AdverseEffectRule()),
        payload,
        Result(False,
               findings=[
                   "Either head of household or authorized representative",
                   "Did not experience any disaster-related adverse effect"])
    )

    payload["is_head_of_household"] = False
    payload["has_inaccessible_liquid_resources"] = True
    assert_result(
        And(AuthorizedRule(), AdverseEffectRule()),
        payload,
        Result(False,
               findings=[
                   "Neither head of household nor authorized representative",
                   "Experienced disaster-related adverse effects"])
    )


@patch('dsnap_rules.dgi_calculator.get_dgi_calculator')
def test_income_and_resource(get_dgi_calculator_mock):
    LIMIT = 500
    ALLOTMENT = 100
    get_dgi_calculator_mock.return_value.get_limit.return_value = LIMIT
    get_dgi_calculator_mock.return_value.get_allotment.return_value = ALLOTMENT

    TOTAL_TAKE_HOME_INCOME = 200
    ACCESSIBLE_LIQUID_RESOURCES = 300
    DEDUCTIBLE_DISASTER_EXPENSES = 50

    VERY_LARGE_TAKE_HOME_INCOME = 2 * LIMIT

    payload = {
        "total_take_home_income": TOTAL_TAKE_HOME_INCOME,
        "accessible_liquid_resources": ACCESSIBLE_LIQUID_RESOURCES,
        "deductible_disaster_expenses": DEDUCTIBLE_DISASTER_EXPENSES,
        "state_or_territory": "CA",
        "size_of_household": 4
    }
    gross_income = (TOTAL_TAKE_HOME_INCOME + ACCESSIBLE_LIQUID_RESOURCES
                    - DEDUCTIBLE_DISASTER_EXPENSES)
    assert_result(
        IncomeAndResourceRule(),
        payload,
        Result(True,
               findings=[
                   f"Gross income {gross_income} within limit of {LIMIT}"],
               metrics={"allotment": ALLOTMENT})
    )

    get_dgi_calculator_mock.assert_called()
    payload["total_take_home_income"] = VERY_LARGE_TAKE_HOME_INCOME
    gross_income = (VERY_LARGE_TAKE_HOME_INCOME + ACCESSIBLE_LIQUID_RESOURCES
                    - DEDUCTIBLE_DISASTER_EXPENSES)
    assert_result(
        IncomeAndResourceRule(),
        payload,
        Result(False,
               findings=[
                   f"Gross income {gross_income} exceeds limit of {LIMIT}"])
    )


def assert_result(rule, payload, expected_result):
    actual_result = rule.execute(payload, config=None)
    assert actual_result == expected_result
