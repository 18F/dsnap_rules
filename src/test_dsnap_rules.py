from copy import deepcopy

from dsnap_rules import (
    AdverseEffectRule,
    AuthorizedRule,
    IncomeAndResourceRule,
)

STOCK_TARGET = {
    "is_head_of_household": False,
    "is_authorized_representative": False,
    "has_lost_or_inaccessible_income": False,
    "has_inaccessible_liquid_resources": False,
    "incurred_deductible_disaster_expenses": False,
}


def test_authorized_rule():
    target = deepcopy(STOCK_TARGET)

    target["is_head_of_household"] = False
    target["is_authorized_representative"] = False
    assert not AuthorizedRule(target)

    target["is_head_of_household"] = True
    target["is_authorized_representative"] = False
    assert AuthorizedRule(target)

    target["is_head_of_household"] = False
    target["is_authorized_representative"] = True
    assert AuthorizedRule(target)

    target["is_head_of_household"] = True
    target["is_authorized_representative"] = True
    assert AuthorizedRule(target)


def test_adverse_effect_rule():
    target = deepcopy(STOCK_TARGET)

    target["has_lost_or_inaccessible_income"] = False
    target["has_inaccessible_liquid_resources"] = False
    target["incurred_deductible_disaster_expenses"] = False
    assert not AdverseEffectRule(target)

    target["has_lost_or_inaccessible_income"] = True
    target["has_inaccessible_liquid_resources"] = False
    target["incurred_deductible_disaster_expenses"] = False
    assert AdverseEffectRule(target)


def test_combined_identity_and_authorized():
    target = deepcopy(STOCK_TARGET)
    target["has_lost_or_inaccessible_income"] = False
    target["incurred_deductible_disaster_expenses"] = True
    target["has_inaccessible_liquid_resources"] = False

    target["is_head_of_household"] = True
    target["is_authorized_representative"] = True
    target["is_identity_verified"] = True
    assert AdverseEffectRule(target) and AuthorizedRule(target)


def test_income_and_resource():
    target = {
        "total_take_home_income": 200,
        "accessible_liquid_resources": 300,
        "deductible_disaster_expenses": 50,
    }
    assert IncomeAndResourceRule(target)

    target["total_take_home_income"] = 2000
    assert not IncomeAndResourceRule(target)
