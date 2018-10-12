from dgi_calculators import get_dgi_calculator
from rules import Rule


class AuthorizedRule(Rule):
    def execute(self):
        return (
            self.payload["is_head_of_household"]
            or self.payload["is_authorized_representative"],
            self.name)


class AdverseEffectRule(Rule):
    """
    Disaster-related adverse effects fall into three categories: loss of
    income, inaccessible resources, and disaster expenses. The household must
    have experienced at least one of these adverse effects in order to be
    eligible.
    """

    def execute(self):
        return (
            self.payload["has_lost_or_inaccessible_income"]
            or self.payload["has_inaccessible_liquid_resources"]
            or self.payload["incurred_deductible_disaster_expenses"],
            self.name)


class IncomeAndResourceRule(Rule):
    """
    The household's take-home income received (or expected to be received)
    during the benefit period plus its accessible liquid resources minus
    disaster related expenses (unreimbursed disaster related expenses paid or
    anticipated to be paid out of pocket during the disaster benefit period)
    shall not exceed the Disaster Gross Income Limit (DGIL).
    """

    def execute(self):
        return (
            self.disaster_gross_income <= self.disaster_gross_income_limit,
            self.name)

    @property
    def disaster_gross_income(self):
        return (
            self.payload["total_take_home_income"]
            + self.payload["accessible_liquid_resources"]
            - self.payload["deductible_disaster_expenses"]
        )

    @property
    def disaster_gross_income_limit(self):
        dgi_calculator = get_dgi_calculator(self.payload["state_or_territory"])
        return dgi_calculator.get_limit(self.payload["size_of_household"])
