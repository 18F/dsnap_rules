from unittest.mock import patch, Mock

from new_rules.config import get_config
from new_rules.rules import And, Result
from new_rules.dsnap.dsnap_rules import (
    AdverseEffectRule,
    AuthorizedRule,
    IncomeAndResourceRule,
    ResidencyRule,
)


def test_authorized_rule():
    payload = {
        "is_head_of_household": False,
        "is_authorized_representative": False,
    }

    assert_result(
        AuthorizedRule(),
        payload,
        Result(False,
               findings=[
                   "Neither head of household nor authorized representative"])
    )

    payload["is_head_of_household"] = True
    payload["is_authorized_representative"] = False
    assert_result(
        AuthorizedRule(),
        payload,
        Result(True,
               findings=[
                   "Either head of household or authorized representative"])
    )

    payload["is_head_of_household"] = False
    payload["is_authorized_representative"] = True
    assert_result(
        AuthorizedRule(),
        payload,
        Result(True,
               findings=[
                   "Either head of household or authorized representative"])
    )


def test_adverse_effect_rule():
    payload = {
        "has_lost_or_inaccessible_income": False,
        "has_inaccessible_liquid_resources": False,
        "incurred_deductible_disaster_expenses": False,
    }

    assert_result(
        AdverseEffectRule(),
        payload,
        Result(False,
               findings=[
                   "Did not experience any disaster-related adverse effect"])
    )

    payload["has_lost_or_inaccessible_income"] = True
    payload["has_inaccessible_liquid_resources"] = False
    payload["incurred_deductible_disaster_expenses"] = False
    assert_result(
        AdverseEffectRule(),
        payload,
        Result(True,
               findings=[
                   "Experienced disaster-related adverse effects"])
    )


def test_residency_rule():
    payload = {
        "resided_in_disaster_area_at_disaster_time": True,
        "worked_in_disaster_area_at_disaster_time": False
    }

    assert_result(
        ResidencyRule(),
        payload,
        Result(True,
               findings=[
                   "Resided or worked in disaster area at disaster time"])
    )

    payload = {
        "resided_in_disaster_area_at_disaster_time": False,
        "worked_in_disaster_area_at_disaster_time": False
    }

    assert_result(
        ResidencyRule(),
        payload,
        Result(False,
               findings=[
                   "Did not reside or work in disaster area at disaster time"])
    )


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


@patch('new_rules.dsnap.dgi_calculator.get_dgi_calculator')
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
    config = get_config()
    actual_result = rule.execute(payload, config)
    assert actual_result == expected_result
