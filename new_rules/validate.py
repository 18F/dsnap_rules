from jsonschema import Draft4Validator


SCHEMA = {
    "$schema": "http://json-schema.org/draft-06/schema#",

    "type": "object",

    "properties": {
        "accessible_liquid_resources": {"type": "number", "minimum": 0},
        "deductible_disaster_expenses": {"type": "number", "minimum": 0},
        "has_inaccessible_liquid_resources": {"type": "boolean"},
        "has_lost_or_inaccessible_income": {"type": "boolean"},
        "incurred_deductible_disaster_expenses": {"type": "boolean"},
        "is_authorized_representative": {"type": "boolean"},
        "is_head_of_household": {"type": "boolean"},
        "resided_in_disaster_area_at_disaster_time": {"type": "boolean"},
        "size_of_household": {"type": "integer", "minimum": 1},
        "state_or_territory": {"type": "string"},
        "total_take_home_income": {"type": "number", "minimum": 0},
        "worked_in_disaster_area_at_disaster_time": {"type": "boolean"},
        "receives_FDPIR_benefits": {"type": "boolean"},
        "receives_TEFAP_food_distribution": {"type": "boolean"},
    },
    "required": [
        "accessible_liquid_resources",
        "deductible_disaster_expenses",
        "has_inaccessible_liquid_resources",
        "has_lost_or_inaccessible_income",
        "incurred_deductible_disaster_expenses",
        "is_head_of_household",
        "resided_in_disaster_area_at_disaster_time",
        "size_of_household",
        "total_take_home_income",
        "worked_in_disaster_area_at_disaster_time",
        "receives_FDPIR_benefits",
        "receives_TEFAP_food_distribution",
    ]
}


def validate(data):
    Draft4Validator(SCHEMA).validate(data)
