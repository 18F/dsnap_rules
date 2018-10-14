class Rule:
    """Rule is a piece of logic that can be executed with a payload to provide a
    Boolean result.  A payload which is `dict` that contains data attributes
    used by the rule.  In addition to the Boolean result, the execution returns
    an `str` object that contains a finding, i.e., more details about the
    success or failure.
    """
    def execute(self, payload):
        pass


class And(Rule):
    def __init__(self, *rules):
        self.rules = rules

    def execute(self, payload):
        overall_result = True
        overall_findings = []
        for rule in self.rules:
            result, finding = rule.execute(payload)
            overall_result = overall_result and result
            overall_findings.append(finding)
        return overall_result, overall_findings
