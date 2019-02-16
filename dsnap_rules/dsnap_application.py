class DSNAPApplication:
    def __init__(self, payload):
        self.__dict__ = payload

    def deductible_disaster_expenses(self):
        total = 0
        for v in self.disaster_expenses.values():
            total += v
        return total
