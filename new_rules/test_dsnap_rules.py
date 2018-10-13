from copy import deepcopy

from dsnap_rules import (
    AdverseEffectRule,
    AuthorizedRule,
    IncomeAndResourceRule,
)

STOCK_PAYLOAD = {
    "is_head_of_household": False,
    "is_authorized_representative": False,
    "has_lost_or_inaccessible_income": False,
    "has_inaccessible_liquid_resources": False,
    "incurred_deductible_disaster_expenses": False,
}


def test_authorized_rule():
    payload = deepcopy(STOCK_PAYLOAD)

    payload["is_head_of_household"] = False
    payload["is_authorized_representative"] = False
    assert_results(AuthorizedRule, payload, False,
                   "Neither head of household nor authorized representative")

    payload["is_head_of_household"] = True
    payload["is_authorized_representative"] = False
    assert_results(AuthorizedRule, payload, True,
                   "Either head of household or authorized representative")

    payload["is_head_of_household"] = False
    payload["is_authorized_representative"] = True
    assert_results(AuthorizedRule, payload, True,
                   "Either head of household or authorized representative")


def test_adverse_effect_rule():
    payload = deepcopy(STOCK_PAYLOAD)

    payload["has_lost_or_inaccessible_income"] = False
    payload["has_inaccessible_liquid_resources"] = False
    payload["incurred_deductible_disaster_expenses"] = False
    assert_results(AdverseEffectRule, payload, False,
                   "Did not experience any disaster-related adverse effect")

    payload["has_lost_or_inaccessible_income"] = True
    payload["has_inaccessible_liquid_resources"] = False
    payload["incurred_deductible_disaster_expenses"] = False
    assert_results(AdverseEffectRule, payload, True,
                   "Experienced disaster-related adverse effects")


def test_combined_identity_and_authorized():
    payload = deepcopy(STOCK_PAYLOAD)
    payload["has_lost_or_inaccessible_income"] = False
    payload["incurred_deductible_disaster_expenses"] = True
    payload["has_inaccessible_liquid_resources"] = False

    payload["is_head_of_household"] = True
    payload["is_authorized_representative"] = True
    payload["is_identity_verified"] = True
    assert AdverseEffectRule(payload) and AuthorizedRule(payload)


def test_income_and_resource():
    TOTAL_TAKE_HOME_INCOME = 200
    ACCESSIBLE_LIQUID_RESOURCES = 300
    DEDUCTIBLE_DISASTER_EXPENSES = 50

    VERY_LARGE_TAKE_HOME_INCOME = 5000

    payload = {
        "total_take_home_income": TOTAL_TAKE_HOME_INCOME,
        "accessible_liquid_resources": ACCESSIBLE_LIQUID_RESOURCES,
        "deductible_disaster_expenses": DEDUCTIBLE_DISASTER_EXPENSES,
        "state_or_territory": "CA",
        "size_of_household": 4
    }
    gross_income = (TOTAL_TAKE_HOME_INCOME + ACCESSIBLE_LIQUID_RESOURCES
                    - DEDUCTIBLE_DISASTER_EXPENSES)
    assert_results(IncomeAndResourceRule, payload, True,
                   f"Gross income {gross_income} within limit of 2818")

    payload["total_take_home_income"] = VERY_LARGE_TAKE_HOME_INCOME
    gross_income = (VERY_LARGE_TAKE_HOME_INCOME + ACCESSIBLE_LIQUID_RESOURCES
                    - DEDUCTIBLE_DISASTER_EXPENSES)
    assert_results(IncomeAndResourceRule, payload, False,
                   f"Gross income {gross_income} exceeds limit of 2818")


def assert_results(rule, payload, expected_result, expected_finding):
    actual_result, actual_finding = rule(payload).execute()
    assert actual_result == expected_result
    assert actual_finding == expected_finding
