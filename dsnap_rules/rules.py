class Result:
    """ A Result object encapsulates a `bool` indicator of success, a list of
    findings, and any metrics that were computed by the executed results.
    """
    def __init__(self, successful, findings, metrics=None):
        if metrics is None:
            metrics = {}
        self.successful = successful
        self.findings = findings
        self.metrics = metrics

    def __eq__(self, other):
        return (
            self.successful == other.successful
            and (
                sorted(self.findings, key=lambda x: x["rule"])
                == sorted(other.findings, key=lambda x: x["rule"]))
            and self.metrics == other.metrics)


class Rule:
    """A Rule is a piece of logic that can be executed with an application and
    a disaster to provide a result. An application is an object that contains
    data attributes used by the rule. A disaster is an instance of Disaster
    which provides information on the disaster for which this D-SNAP is being
    run.
    """
    def execute(self, application, disaster):
        pass

    def assemble_findings(self, result, text):
        return [{
            "rule": self.__class__.__name__,
            "succeeded": result,
            "text": text
        }]


class SimplePredicateRule(Rule):
    """A SimplePredicateRule is a convenience class used when the predicate is
    simple and the findings for success and failure are static strings.
    """

    def execute(self, application, disaster):
        result = self.predicate(application, disaster)
        finding = self.success_finding if result else self.failure_finding
        return Result(result, self.assemble_findings(result, finding))

    def predicate(self, application, disaster):
        pass


class And(Rule):
    def __init__(self, *rules):
        self.rules = rules

    def execute(self, application, disaster):
        overall_success = True
        overall_findings = []
        overall_metrics = {}
        for rule in self.rules:
            result = rule.execute(application, disaster)
            overall_success = overall_success and result.successful
            overall_findings.extend(result.findings)
            overall_metrics.update(result.metrics)
        return Result(overall_success, overall_findings, overall_metrics)
