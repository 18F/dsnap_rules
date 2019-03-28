from . import income_allotment_calculator
from .rules import Result, Rule, SimplePredicateRule


class AuthorizedRule(SimplePredicateRule):
    success_finding = "Either head of household or authorized representative"
    failure_finding = "Neither head of household nor authorized representative"

    def predicate(self, application, disaster):
        return (application.is_head_of_household
                or application.is_authorized_representative)


class FoodPurchaseRule(SimplePredicateRule):
    """
    The household must plan on purchasing food during the disaster benefit
    period or have purchased food during that time if the benefit period has
    passed.
    """
    success_finding = "Either purchased or plans to purchase food during "\
                      "benefit period"
    failure_finding = "Neither purchased nor plans to purchase food during "\
                      "benefit period"

    def predicate(self, application, disaster):
        return application.purchased_or_plans_to_purchase_food


class AdverseEffectRule(SimplePredicateRule):
    """
    Disaster-related adverse effects fall into three categories: loss of
    income, inaccessible resources, and disaster expenses. The household must
    have experienced at least one of these adverse effects in order to be
    eligible.
    """
    success_finding = "Experienced disaster-related adverse effects"
    failure_finding = "Did not experience any disaster-related adverse "\
        "effect, or they experienced only food loss and this disaster "\
        "does not allow food loss alone"

    def predicate(self, application, disaster):
        return (
            application.has_lost_or_inaccessible_income
            or application.has_inaccessible_liquid_resources
            or self.incurred_deductible_disaster_expenses(
                application, disaster)
        )

    def incurred_deductible_disaster_expenses(self, application, disaster):
        if disaster.uses_DSED:
            return False
        else:
            return application.deductible_disaster_expenses(
                disaster.allows_food_loss_alone) > 0


class DisasterAreaResidencyRule(Rule):
    """
    In most cases, the household must have lived in the disaster area at the
    time of the disaster. States may also choose to extend eligibility to those
    who worked in the disaster area at the time of the disaster.
    """

    resided_finding = "Resided in disaster area at disaster time"
    worked_ineligible_finding = "Worked in disaster area at disaster "\
        "time but only residents are eligible"
    worked_eligible_finding = "Worked in disaster area at disaster time "\
        "and those who worked are eligible to receive benefits for this "\
        "disaster"
    failure_finding = "Did not reside or work in disaster area at disaster "\
                      "time"

    def execute(self, application, disaster):
        result = False
        if application.resided_in_disaster_area_at_disaster_time:
            finding = self.resided_finding
            result = True
        elif application.worked_in_disaster_area_at_disaster_time:
            if disaster.residency_required:
                finding = self.worked_ineligible_finding
                result = False
            else:
                finding = self.worked_eligible_finding
                result = True
        else:
            finding = self.failure_finding
            result = False

        return Result(result, self.assemble_findings(result, finding))


class SNAPSupplementalBenefitsRule(SimplePredicateRule):
    """
    Supplemental benefits provide parity between new D-SNAP households
    and ongoing clients, who are not eligible for D-SNAP benefits.
    """
    success_finding = "Does not receive benefits from SNAP"
    failure_finding = "SNAP beneficiaries should apply for supplemental "\
                      "benefits through SNAP"

    def predicate(self, application, disaster):
        return not application.receives_SNAP_benefits


class IncomeAndResourceRule(Rule):
    """
    The household's take-home income received (or expected to be received)
    during the benefit period plus its accessible liquid resources minus
    disaster related expenses (unreimbursed disaster related expenses paid or
    anticipated to be paid out of pocket during the disaster benefit period)
    shall not exceed the Disaster Gross Income Limit (DGIL).

    With FNS approval, a State may choose to utilize a Disaster Standard
    Expense Deduction (DSED) in lieu of actual disaster expenses incurred by a
    household, provided that food loss alone is not the only qualifying
    expense.
    """

    def execute(self, application, disaster):
        gross_income = self.disaster_gross_income(application, disaster)
        income_limit, allotment = self.get_limit_and_allotment(
            application, disaster)
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
        return Result(result, self.assemble_findings(result, finding), metrics)

    def disaster_gross_income(self, application, disaster):
        return (
            application.total_take_home_income
            + application.accessible_liquid_resources
            - (0 if disaster.uses_DSED
               else self.food_loss_adjusted_disaster_expenses(
                   application, disaster))
        )

    def food_loss_adjusted_disaster_expenses(self, application, disaster):
        if disaster.allows_food_loss_alone:
            return application.deductible_disaster_expenses(True)
        disaster_expenses = application.deductible_disaster_expenses(False)
        if disaster_expenses > 0:
            disaster_expenses += application.food_loss()
        return disaster_expenses

    def get_limit_and_allotment(self, application, disaster):
        calculator = income_allotment_calculator.get_calculator(
                        disaster)
        return (
            calculator.get_limit(application.size_of_household),
            calculator.get_allotment(application.size_of_household)
        )
