from jsonschema import Draft4Validator
from jsonschema.exceptions import ValidationError

SCHEMA = {
    "$schema": "http://json-schema.org/draft-06/schema#",

    "type": "object",

    "properties": {
        "accessible_liquid_resources": {"type": "number", "minimum": 0},
        "disaster_expenses": {"type": "object", "properties": {
            "food_loss": {"type": "number", "minimum": 0},
            "home_or_business_repairs": {"type": "number", "minimum": 0},
            "temporary_shelter_expenses": {"type": "number", "minimum": 0},
            "evacuation_expenses": {"type": "number", "minimum": 0},
            "home_or_business_property_protection": {
                "type": "number", "minimum": 0},
            "personal_injury_medical_expenses": {
                "type": "number", "minimum": 0},
            "disaster_related_funeral_expenses": {
                "type": "number", "minimum": 0},
            "disaster_related_pet_boarding_fees": {
                "type": "number", "minimum": 0},
            "expenses_related_to_replacing_items": {
                "type": "number", "minimum": 0},
            "fuel_for_primary_heating_source": {
                "type": "number", "minimum": 0},
            "disaster_damaged_vehicle_expenses": {
                "type": "number", "minimum": 0},
            "storage_expenses": {"type": "number", "minimum": 0},
            }
        },
        "disaster_request_no": {"type": "string"},
        "has_inaccessible_liquid_resources": {"type": "boolean"},
        "has_lost_or_inaccessible_income": {"type": "boolean"},
        "incurred_deductible_disaster_expenses": {"type": "boolean"},
        "is_authorized_representative": {"type": "boolean"},
        "is_head_of_household": {"type": "boolean"},
        "resided_in_disaster_area_at_disaster_time": {"type": "boolean"},
        "plans_to_purchase_food_during_benefit_period": {"type": "boolean"},
        "purchased_food_during_benefit_period": {"type": "boolean"},
        "size_of_household": {"type": "integer", "minimum": 1},
        "total_take_home_income": {"type": "number", "minimum": 0},
        "worked_in_disaster_area_at_disaster_time": {"type": "boolean"},
        "receives_FDPIR_benefits": {"type": "boolean"},
        "receives_TEFAP_food_distribution": {"type": "boolean"},
        "receives_SNAP_benefits": {"type": "boolean"},
    },
    "required": [
        "accessible_liquid_resources",
        "disaster_request_no",
        "has_inaccessible_liquid_resources",
        "has_lost_or_inaccessible_income",
        "incurred_deductible_disaster_expenses",
        "is_head_of_household",
        "plans_to_purchase_food_during_benefit_period",
        "purchased_food_during_benefit_period",
        "resided_in_disaster_area_at_disaster_time",
        "size_of_household",
        "total_take_home_income",
        "worked_in_disaster_area_at_disaster_time",
        "receives_FDPIR_benefits",
        "receives_TEFAP_food_distribution",
        "receives_SNAP_benefits",
    ]
}


def validate(data):
    error_messages = [
        error.message for error in Draft4Validator(SCHEMA).iter_errors(data)]
    if error_messages:
        raise ValidationError(message=error_messages)
