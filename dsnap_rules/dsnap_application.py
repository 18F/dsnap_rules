class DSNAPApplication:
    def __init__(self, payload):
        self.__dict__ = payload

    def deductible_disaster_expenses(self, include_food_loss):
        total = 0
        for (k, v) in self.disaster_expenses.items():
            if k == "food_loss" and not include_food_loss:
                continue
            total += v
        return total

    def food_loss(self):
        return self.disaster_expenses.get('food_loss', 0)
