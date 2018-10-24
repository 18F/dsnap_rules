import pytest

from jsonschema.exceptions import ValidationError
from new_rules.validate import validate


def test_good_data():
    validate({
        "is_head_of_household": True,
        "has_lost_or_inaccessible_income": False,
        "has_inaccessible_liquid_resources": False,
        "incurred_deductible_disaster_expenses": False,
        "size_of_household": 2,
        "total_take_home_income": 10,
        "accessible_liquid_resources": 0,
        "deductible_disaster_expenses": 4.5,
    })


def test_missing_required_field():
    with pytest.raises(ValidationError):
        validate({
            "is_head_of_household": True,
            "has_lost_or_inaccessible_income": False,
            "incurred_deductible_disaster_expenses": False,
        })
