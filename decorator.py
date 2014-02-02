'''Decorator pattern.

- Composition > inheritance
- Classes should be open for extension but closed for modification
- Decorator allows behavior of *objects* to be changed at *runtime*;
    good alternative to subclassing
'''


class Espresso:

    @property
    def description(self):
        return "Espresso"

    def cost(self):
        return 1.99


class HouseBlend:

    @property
    def description(self):
        return "House Blend Coffee"

    def cost(self):
        return 0.89

# Modified from HFDP: No need to define abstract beverage supertype just to share
# type between wrappers and the wrappees
class CondimentDecorator:
    '''Wraps a beverage object, modifying its cost and description.'''
    NAME = ''
    COST = 0.0

    def __init__(self, beverage):
        self.beverage = beverage  # Wraps a Beverage object

    # Modified from HFDP: ``description`` and ``cost`` are shared among the
    # concrete decorators, so subclasses only need to specify
    # COST and NAME
    @property
    def description(self):
        return ", ".join([self.beverage.description, self.NAME])

    def cost(self):
        return self.COST + self.beverage.cost()


class with_mocha(CondimentDecorator):
    NAME = "Mocha"
    COST = 0.20


class with_whip(CondimentDecorator):
    NAME = "Whip"
    COST = 0.10


def test():
    beverage = Espresso()
    assert beverage.description == "Espresso"
    wrapped_beverage = with_mocha(beverage)
    assert wrapped_beverage.cost() == 2.19
    assert wrapped_beverage.description == "Espresso, Mocha"
    multiwrapped = with_whip(wrapped_beverage)
    assert multiwrapped.cost() == 2.29
    assert multiwrapped.description == "Espresso, Mocha, Whip"

if __name__ == '__main__':
    test()
