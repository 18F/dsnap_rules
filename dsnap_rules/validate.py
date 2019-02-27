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
                "home_or_business_property_protection": {
                    "type": "number", "minimum": 0},
                "personal_injury_medical": {
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
                "storage_expenses": {
                    "type": "number", "minimum": 0},
            },
            "additionalProperties": False
        },
        "disaster_request_no": {"type": "string"},
        "has_inaccessible_liquid_resources": {"type": "boolean"},
        "has_lost_or_inaccessible_income": {"type": "boolean"},
        "is_authorized_representative": {"type": "boolean"},
        "is_head_of_household": {"type": "boolean"},
        "resided_in_disaster_area_at_disaster_time": {"type": "boolean"},
        "purchased_or_plans_to_purchase_food": {"type": "boolean"},
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
        "disaster_expenses",
        "has_inaccessible_liquid_resources",
        "has_lost_or_inaccessible_income",
        "is_head_of_household",
        "purchased_or_plans_to_purchase_food",
        "receives_FDPIR_benefits",
        "receives_SNAP_benefits",
        "receives_TEFAP_food_distribution",
        "resided_in_disaster_area_at_disaster_time",
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
