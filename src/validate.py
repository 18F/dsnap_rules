from jsonschema import Draft4Validator


SCHEMA = {
    "$schema": "http://json-schema.org/draft-06/schema#",

    "type": "object",

    "properties": {
        "is_head_of_household": {"type": "boolean"},
        "is_authorized_representative": {"type": "boolean"},
        "has_lost_or_inaccessible_income": {"type": "boolean"},
        "has_inaccessible_liquid_resources": {"type": "boolean"},
        "incurred_deductible_disaster_expenses": {"type": "boolean"},
        "size_of_household": {"type": "integer", "minimum": 1},
        "total_take_home_income": {"type": "number", "minimum": 0},
        "accessible_liquid_resources": {"type": "number", "minimum": 0},
        "deductible_disaster_expenses": {"type": "number", "minimum": 0},
    },
    "required": [
        "is_head_of_household",
        "has_lost_or_inaccessible_income",
        "has_inaccessible_liquid_resources",
        "incurred_deductible_disaster_expenses",
        "size_of_household",
        "total_take_home_income",
        "accessible_liquid_resources",
        "deductible_disaster_expenses",
    ]
}


def validate(data):
    Draft4Validator(SCHEMA).validate(data)
