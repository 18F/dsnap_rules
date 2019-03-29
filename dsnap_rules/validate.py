from jsonschema import Draft7Validator

SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",

    "type": "object",

    "properties": {
        "accessible_liquid_resources": {"type": "number", "minimum": 0},
        "disaster_expenses": {
            "type": "object",
            "properties": {
                "food_loss": {
                    "type": "number", "minimum": 0},
                "home_or_business_repairs": {
                    "type": "number", "minimum": 0},
                "temporary_shelter_expenses": {
                    "type": "number", "minimum": 0},
                "evacuation_expenses": {
                    "type": "number", "minimum": 0},
                "other": {
                    "type": "number", "minimum": 0},
            },
            "additionalProperties": False
        },
        "disaster_id": {"type": "integer"},
        "has_inaccessible_liquid_resources": {"type": "boolean"},
        "has_lost_or_inaccessible_income": {"type": "boolean"},
        "is_authorized_representative": {"type": "boolean"},
        "is_head_of_household": {"type": "boolean"},
        "resided_in_disaster_area_at_disaster_time": {"type": "boolean"},
        "purchased_or_plans_to_purchase_food": {"type": "boolean"},
        "size_of_household": {"type": "integer", "minimum": 1},
        "total_take_home_income": {"type": "number", "minimum": 0},
        "worked_in_disaster_area_at_disaster_time": {"type": "boolean"},
        "receives_SNAP_benefits": {"type": "boolean"},
        "residence_state": {"type": "string"},
    },
    "required": [
        "accessible_liquid_resources",
        "disaster_id",
        "disaster_expenses",
        "has_inaccessible_liquid_resources",
        "has_lost_or_inaccessible_income",
        "is_head_of_household",
        "purchased_or_plans_to_purchase_food",
        "receives_SNAP_benefits",
        "resided_in_disaster_area_at_disaster_time",
        "residence_state",
        "size_of_household",
        "total_take_home_income",
        "worked_in_disaster_area_at_disaster_time",
    ],
    "additionalProperties": False
}


def validate(data):
    error_messages = [
        error.message for error in Draft7Validator(SCHEMA).iter_errors(data)]
    if error_messages:
        return False, error_messages
    else:
        return True, []
