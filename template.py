"""Template method pattern.

- Define skeleton of an algorithm, defer some steps to subclasses.
- "Don't call me, we'll call you": Don't allow subclasses to depend on superclasses.
    Only allow superclasses to use subclasses for concrete implementation details.
"""
from abc import ABCMeta, abstractmethod

class CaffeineBeverage(metaclass=ABCMeta):

    def prepare_recipe(self):  # Template method
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        if self.customer_wants_condiments():
            self.add_condiments()

    @abstractmethod
    def brew(self):
        return

    @abstractmethod
    def add_condiments(self):
        return

    def boil_water(self):
        return "Water is boiled"

    def pour_in_cup(self):
        return "Drink is poured"

    def customer_wants_condiments(self):  # A hook (optional override)
        return True

class Coffee(CaffeineBeverage):

    def brew(self):
        return "Brewed coffee grinds"

    def add_condiments(self):
        return "Added sugar and milk"

    def customer_wants_condiments(self):
        answer = input("Sugar and milk? ")
        return answer.lower().startswith("y")

class Tea(CaffeineBeverage):

    def brew(self):
        return 'Steeped teabag'

    def add_condiments(self):
        return 'Added lemon'
