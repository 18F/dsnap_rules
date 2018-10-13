class Rule:
    """Rule is a piece of logic that can be executed to provide a Boolean result.
    A rule accepts a payload which is `dict` that contains data attributes used
    by the rule.  In addition, the execution returns an `str` object that
    contains a finding, i.e., more details about the success or failure.
    """
    def __init__(self, payload, name=None):
        self.payload = payload
        self.name = name

    def __bool__(self):
        result, *rest = self.execute()
        return result

    def execute(self):
        pass
