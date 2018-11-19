class Result:
    """ A Result object encapsulates a `bool` indicator of success, a list of
    findings, and any metrics that were computed by the executed results.
    """
    def __init__(self, successful, findings, metrics={}):
        self.successful = successful
        self.findings = findings
        self.metrics = metrics

    def __eq__(self, other):
        return (
            self.successful == other.successful
            and sorted(self.findings) == sorted(other.findings)
            and self.metrics == other.metrics)


class Rule:
    """A Rule is a piece of logic that can be executed with a payload and a config
    to provide a result. A payload is a `dict` that contains data attributes
    used by the rule. A config is an instance of Config which provides
    contextual environmental information for the rule.
    """
    def execute(self, payload, config):
        pass


class SimplePredicateRule(Rule):
    """A SimplePredicateRule is a convenience class used when the predicate is
    simple and the findings for success and failure are static strings.
    """

    def execute(self, payload, config):
        result = self.predicate(payload, config)
        finding = self.success_finding if result else self.failure_finding
        return Result(result, [finding])


class And(Rule):
    def __init__(self, *rules):
        self.rules = rules

    def execute(self, payload, config):
        overall_success = True
        overall_findings = []
        overall_metrics = {}
        for rule in self.rules:
            result = rule.execute(payload, config)
            overall_success = overall_success and result.successful
            overall_findings.extend(result.findings)
            overall_metrics.update(result.metrics)
        return Result(overall_success, overall_findings, overall_metrics)