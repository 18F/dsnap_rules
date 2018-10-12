class Rule:
    def __init__(self, payload, name=None):
        self.payload = payload
        self.name = name

    def __bool__(self):
        result, *rest = self.execute()
        return result

    def execute(self):
        pass
