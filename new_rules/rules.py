class Result:
    """ A Result object encapsulates a `bool` indicator of success, a list of
    findings, and any metrics that were computed by the executed results.
    """
    def __init__(self, successful, findings, metrics={}):
        self.successful = successful
        self.findings = findings
        self.metrics = metrics


class Rule:
    """Rule is a piece of logic that can be executed with a payload to provide a
    result.  A payload which is `dict` that contains data attributes
    used by the rule.
    """
    def execute(self, payload):
        pass


class And(Rule):
    def __init__(self, *rules):
        self.rules = rules

    def execute(self, payload):
        overall_success = True
        overall_findings = []
        overall_metrics = {}
        for rule in self.rules:
            result = rule.execute(payload)
            overall_success = overall_success and result.successful
            overall_findings.extend(result.findings)
            overall_metrics.update(result.metrics)
        return Result(overall_success, overall_findings, overall_metrics)
