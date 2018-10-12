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
    assert not AuthorizedRule(payload)

    payload["is_head_of_household"] = True
    payload["is_authorized_representative"] = False
    assert AuthorizedRule(payload)

    payload["is_head_of_household"] = False
    payload["is_authorized_representative"] = True
    assert AuthorizedRule(payload)

    payload["is_head_of_household"] = True
    payload["is_authorized_representative"] = True
    assert AuthorizedRule(payload)


def test_adverse_effect_rule():
    payload = deepcopy(STOCK_PAYLOAD)

    payload["has_lost_or_inaccessible_income"] = False
    payload["has_inaccessible_liquid_resources"] = False
    payload["incurred_deductible_disaster_expenses"] = False
    assert not AdverseEffectRule(payload)

    payload["has_lost_or_inaccessible_income"] = True
    payload["has_inaccessible_liquid_resources"] = False
    payload["incurred_deductible_disaster_expenses"] = False
    assert AdverseEffectRule(payload)


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
    payload = {
        "total_take_home_income": 200,
        "accessible_liquid_resources": 300,
        "deductible_disaster_expenses": 50,
        "state_or_territory": "CA",
        "size_of_household": 4
    }
    assert IncomeAndResourceRule(payload)

    payload["total_take_home_income"] = 5000
    assert not IncomeAndResourceRule(payload)
