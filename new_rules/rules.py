class Rule:
    """Rule is a piece of logic that can be executed with a payload to provide a
    Boolean result.  A payload which is `dict` that contains data attributes
    used by the rule.  In addition to the Boolean result, the execution returns
    an `str` object that contains a finding, i.e., more details about the
    success or failure.
    """
    def execute(self, payload):
        pass
