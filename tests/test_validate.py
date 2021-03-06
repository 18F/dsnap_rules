from dsnap_rules.validate import validate


def test_good_data():
    valid, messages = validate({
        "disaster_id": 42,
        "disaster_expenses": {
            "food_loss": 0
        },
        "is_head_of_household": True,
        "has_lost_or_inaccessible_income": False,
        "has_inaccessible_liquid_resources": False,
        "purchased_or_plans_to_purchase_food": True,
        "resided_in_disaster_area_at_disaster_time": True,
        "worked_in_disaster_area_at_disaster_time": False,
        "size_of_household": 2,
        "total_take_home_income": 10,
        "accessible_liquid_resources": 0,
        "receives_SNAP_benefits": False,
        "residence_state": "CA",
    })
    assert valid is True
    assert len(messages) == 0


def test_missing_required_field():
    valid, messages = validate({
        "is_head_of_household": True,
        "has_lost_or_inaccessible_income": False,
        "residence_state": "CA",
    })
    assert valid is False
    assert set(messages) == set([
        "'accessible_liquid_resources' is a required property",
        "'disaster_id' is a required property",
        "'disaster_expenses' is a required property",
        "'has_inaccessible_liquid_resources' is a required property",
        "'purchased_or_plans_to_purchase_food' is a required property",
        "'resided_in_disaster_area_at_disaster_time' is a required property",
        "'size_of_household' is a required property",
        "'total_take_home_income' is a required property",
        "'worked_in_disaster_area_at_disaster_time' is a required property",
        "'receives_SNAP_benefits' is a required property"
    ])
