import pytest

from jsonschema.exceptions import ValidationError
from new_rules.validate import validate


def test_good_data():
    validate({
        "is_head_of_household": True,
        "has_lost_or_inaccessible_income": False,
        "has_inaccessible_liquid_resources": False,
        "incurred_deductible_disaster_expenses": False,
        "plans_to_purchase_food_during_benefit_period": True,
        "purchased_food_during_benefit_period": False,
        "resided_in_disaster_area_at_disaster_time": True,
        "worked_in_disaster_area_at_disaster_time": False,
        "size_of_household": 2,
        "total_take_home_income": 10,
        "accessible_liquid_resources": 0,
        "deductible_disaster_expenses": 4.5,
        "receives_FDPIR_benefits": True,
        "receives_TEFAP_food_distribution": False,
    })


def test_missing_required_field():
    with pytest.raises(ValidationError):
        validate({
            "is_head_of_household": True,
            "has_lost_or_inaccessible_income": False,
            "incurred_deductible_disaster_expenses": False,
        })
