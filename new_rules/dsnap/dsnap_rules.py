from . import dgi_calculator
from ..rules import Rule


class AuthorizedRule(Rule):
    def execute(self, payload):
        result = (payload["is_head_of_household"]
                  or payload["is_authorized_representative"])
        if result:
            finding = "Either head of household or authorized representative"
        else:
            finding = "Neither head of household nor authorized representative"
        return (result, finding)


class AdverseEffectRule(Rule):
    """
    Disaster-related adverse effects fall into three categories: loss of
    income, inaccessible resources, and disaster expenses. The household must
    have experienced at least one of these adverse effects in order to be
    eligible.
    """

    def execute(self, payload):
        result = (
            payload["has_lost_or_inaccessible_income"]
            or payload["has_inaccessible_liquid_resources"]
            or payload["incurred_deductible_disaster_expenses"])
        if result:
            finding = "Experienced disaster-related adverse effects"
        else:
            finding = "Did not experience any disaster-related adverse effect"
        return (result, finding)


class IncomeAndResourceRule(Rule):
    """
    The household's take-home income received (or expected to be received)
    during the benefit period plus its accessible liquid resources minus
    disaster related expenses (unreimbursed disaster related expenses paid or
    anticipated to be paid out of pocket during the disaster benefit period)
    shall not exceed the Disaster Gross Income Limit (DGIL).
    """

    def execute(self, payload):
        disaster_gross_income = self.disaster_gross_income(payload)
        disaster_gross_income_limit = self.disaster_gross_income_limit(payload)
        result = disaster_gross_income <= disaster_gross_income_limit
        if result:
            finding = (
                f"Gross income {disaster_gross_income} within limit of "
                f"{disaster_gross_income_limit}"
            )
        else:
            finding = (
                f"Gross income {disaster_gross_income} exceeds limit of "
                f"{disaster_gross_income_limit}"
            )
        return (result, finding)

    def disaster_gross_income(self, payload):
        return (
            payload["total_take_home_income"]
            + payload["accessible_liquid_resources"]
            - payload["deductible_disaster_expenses"]
        )

    def disaster_gross_income_limit(self, payload):
        calculator = dgi_calculator.get_dgi_calculator(
                        payload["state_or_territory"])
        return calculator.get_limit(payload["size_of_household"])
