from . import dgi_calculator
from ..rules import Rule, Result


class AuthorizedRule(Rule):
    def execute(self, payload, config):
        result = (payload["is_head_of_household"]
                  or payload["is_authorized_representative"])
        if result:
            finding = "Either head of household or authorized representative"
        else:
            finding = "Neither head of household nor authorized representative"
        return Result(result, [finding])


class AdverseEffectRule(Rule):
    """
    Disaster-related adverse effects fall into three categories: loss of
    income, inaccessible resources, and disaster expenses. The household must
    have experienced at least one of these adverse effects in order to be
    eligible.
    """

    def execute(self, payload, config):
        result = (
            payload["has_lost_or_inaccessible_income"]
            or payload["has_inaccessible_liquid_resources"]
            or payload["incurred_deductible_disaster_expenses"])
        if result:
            finding = "Experienced disaster-related adverse effects"
        else:
            finding = "Did not experience any disaster-related adverse effect"
        return Result(result, [finding])


class ResidencyRule(Rule):
    """
    In most cases, the household must have lived in the disaster area at the
    time of the disaster. States may also choose to extend eligibility to those
    who worked in the disaster area at the time of the disaster.
    """

    def execute(self, payload, config):
        result = (
            payload["resided_in_disaster_area_at_disaster_time"]
            or (
                payload["worked_in_disaster_area_at_disaster_time"]
                and config.worked_in_disaster_area_is_dnsap_eligible)
        )
        if result:
            finding = "Resided or worked in disaster area at disaster time"
        else:
            finding = "Did not reside or work in disaster area at disaster "\
                      "time"
        return Result(result, [finding])


class IncomeAndResourceRule(Rule):
    """
    The household's take-home income received (or expected to be received)
    during the benefit period plus its accessible liquid resources minus
    disaster related expenses (unreimbursed disaster related expenses paid or
    anticipated to be paid out of pocket during the disaster benefit period)
    shall not exceed the Disaster Gross Income Limit (DGIL).
    """

    def execute(self, payload, config):
        gross_income = self.disaster_gross_income(payload)
        income_limit, allotment = self.get_limit_and_allotment(payload)
        result = gross_income <= income_limit
        if result:
            finding = (
                f"Gross income {gross_income} within limit of "
                f"{income_limit}"
            )
            metrics = {"allotment": allotment}
        else:
            finding = (
                f"Gross income {gross_income} exceeds limit of "
                f"{income_limit}"
            )
            metrics = {}
        return Result(result, [finding], metrics)

    def disaster_gross_income(self, payload):
        return (
            payload["total_take_home_income"]
            + payload["accessible_liquid_resources"]
            - payload["deductible_disaster_expenses"]
        )

    def get_limit_and_allotment(self, payload):
        calculator = dgi_calculator.get_dgi_calculator(
                        payload["state_or_territory"])
        return (
            calculator.get_limit(payload["size_of_household"]),
            calculator.get_allotment(payload["size_of_household"])
        )
