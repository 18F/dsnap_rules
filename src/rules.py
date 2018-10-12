from abc import ABCMeta, abstractmethod


class Rule(metaclass=ABCMeta):
    def __init__(self, payload, name=None):
        self.payload = payload
        self.name = name

    def __bool__(self):
        result, *rest = self.execute()
        return result

    @abstractmethod
    def execute(self):
        pass
