from . import dgi_calculator
from ..rules import Rule, Result, SimplePredicateRule


class AuthorizedRule(SimplePredicateRule):
    success_finding = "Either head of household or authorized representative"
    failure_finding = "Neither head of household nor authorized representative"

    def predicate(self, payload, config):
        return (payload["is_head_of_household"]
                or payload["is_authorized_representative"])


class AdverseEffectRule(SimplePredicateRule):
    """
    Disaster-related adverse effects fall into three categories: loss of
    income, inaccessible resources, and disaster expenses. The household must
    have experienced at least one of these adverse effects in order to be
    eligible.
    """
    success_finding = "Experienced disaster-related adverse effects"
    failure_finding = "Did not experience any disaster-related adverse effect"

    def predicate(self, payload, config):
        return (
            payload["has_lost_or_inaccessible_income"]
            or payload["has_inaccessible_liquid_resources"]
            or payload["incurred_deductible_disaster_expenses"])


class ResidencyRule(SimplePredicateRule):
    """
    In most cases, the household must have lived in the disaster area at the
    time of the disaster. States may also choose to extend eligibility to those
    who worked in the disaster area at the time of the disaster.
    """

    success_finding = "Resided or worked in disaster area at disaster time"
    failure_finding = "Did not reside or work in disaster area at disaster "\
                      "time"

    def predicate(self, payload, config):
        return (
            payload["resided_in_disaster_area_at_disaster_time"]
            or (
                payload["worked_in_disaster_area_at_disaster_time"]
                and config.worked_in_disaster_area_is_dnsap_eligible)
        )


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
