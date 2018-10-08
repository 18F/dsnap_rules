from rules import Rule


class AuthorizedRule(Rule):
    def execute(self):
        return (
            self.target["is_head_of_household"]
            or self.target["is_authorized_representative"],
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
            self.target["has_lost_or_inaccessible_income"]
            or self.target["has_inaccessible_liquid_resources"]
            or self.target["incurred_deductible_disaster_expenses"],
            self.name)
