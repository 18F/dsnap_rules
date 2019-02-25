from dsnap_rules.validate import validate


def test_good_data():
    valid, messages = validate({
        "disaster_request_no": "DR-1",
        "is_head_of_household": True,
        "has_lost_or_inaccessible_income": False,
        "has_inaccessible_liquid_resources": False,
        "incurred_deductible_disaster_expenses": False,
        "purchased_or_plans_to_purchase_food": True,
        "resided_in_disaster_area_at_disaster_time": True,
        "worked_in_disaster_area_at_disaster_time": False,
        "size_of_household": 2,
        "total_take_home_income": 10,
        "accessible_liquid_resources": 0,
        "deductible_disaster_expenses": 4.5,
        "receives_FDPIR_benefits": True,
        "receives_TEFAP_food_distribution": False,
        "receives_SNAP_benefits": False,
    })
    assert valid is True
    assert len(messages) == 0


def test_missing_required_field():
    valid, messages = validate({
            "is_head_of_household": True,
            "has_lost_or_inaccessible_income": False,
            "incurred_deductible_disaster_expenses": False,
    })
    assert valid is False
    assert set(messages) == set([
        "'accessible_liquid_resources' is a required property",
        "'disaster_request_no' is a required property",
        "'has_inaccessible_liquid_resources' is a required property",
        "'purchased_or_plans_to_purchase_food' is a required property",
        "'resided_in_disaster_area_at_disaster_time' is a required property",
        "'size_of_household' is a required property",
        "'total_take_home_income' is a required property",
        "'worked_in_disaster_area_at_disaster_time' is a required property",
        "'receives_FDPIR_benefits' is a required property",
        "'receives_TEFAP_food_distribution' is a required property",
        "'receives_SNAP_benefits' is a required property"
    ])
