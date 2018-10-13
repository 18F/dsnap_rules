import dgi_calculator
from rules import Rule


class AuthorizedRule(Rule):
    def execute(self):
        result = (self.payload["is_head_of_household"]
                  or self.payload["is_authorized_representative"])
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

    def execute(self):
        result = (
            self.payload["has_lost_or_inaccessible_income"]
            or self.payload["has_inaccessible_liquid_resources"]
            or self.payload["incurred_deductible_disaster_expenses"])
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

    def execute(self):
        result = self.disaster_gross_income <= self.disaster_gross_income_limit
        if result:
            finding = (
                f"Gross income {self.disaster_gross_income} within limit of "
                f"{self.disaster_gross_income_limit}"
            )
        else:
            finding = (
                f"Gross income {self.disaster_gross_income} exceeds limit of "
                f"{self.disaster_gross_income_limit}"
            )
        return (result, finding)

    @property
    def disaster_gross_income(self):
        return (
            self.payload["total_take_home_income"]
            + self.payload["accessible_liquid_resources"]
            - self.payload["deductible_disaster_expenses"]
        )

    @property
    def disaster_gross_income_limit(self):
        calculator = dgi_calculator.get_dgi_calculator(self.payload["state_or_territory"])
        return calculator.get_limit(self.payload["size_of_household"])
