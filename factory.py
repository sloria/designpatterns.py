"""Factory pattern (abstract factory and factory method).

- Factory method - defines interface for creating *one* object; subclasses decide
                    which class to instantiate. Decouples client code from the
                    concrete product classes.
- Abstract factory - provides interface for creating *related* objects.
- Depend upon abstractions, not concrete classes
"""

from abc import ABCMeta, abstractmethod

# An abstract factory
# May not always be necessary. In Python, generally don't need to
# create superclasses just to share type
class PizzaIngredientFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_dough(self): return
    @abstractmethod
    def create_sauce(self): return
    @abstractmethod
    def create_cheese(self): return
    @abstractmethod
    def create_pepperoni(self): return


# Concrete ingredient factory
class NYPizzaIngredientFactory(PizzaIngredientFactory):
    def create_dough(self):
        return "ThinCrustDough"  # This would actually be an instantiated Dough object
                                 # intead of just a string

    def create_sauce(self):
        return "MarinaraSauce"

    def create_cheese(self):
        return "ReggianoCheese"

    def create_pepperoni(self):
        return "SlicedPepperoni"

class ChicagoPizzaIngredientFactory(PizzaIngredientFactory):
    def create_dough(self):
        return "ThickCrustDough"

    def create_sauce(self):
        return "PlumTomatoSauce"

    def create_cheese(self):
        return "MozzarellaCheese"

    def create_pepperoni(self):
        return "SlicedPepperoni"

# Abstract product class
class Pizza(metaclass=ABCMeta):
    name = ''
    dough = ''
    sauce =''
    toppings = []

    def __init__(self, ingredient_factory):
        # Composing a factory decouples the Pizza class
        # from regional ingredient differences
        self.ingredient_factory = ingredient_factory

    @abstractmethod
    def prepare(self):
        """Collect ingredients from an ingredient factory and prepare the pizza.
        """
        return

    def bake(self):
        print("Bake for 25 minutes at 350")

    def cut(self):
        print('Cutting the pizza into diagonal slices')

    def box(self):
        print("Place pizza in official PizzaStore box")

# Concrete Pizza classes
class CheesePizza(Pizza):
    def prepare(self):
        self.dough = self.ingredient_factory.create_dough()
        self.sauce = self.ingredient_factory.create_sauce()
        self.cheese = self.ingredient_factory.create_cheese()


class PepperoniPizza(Pizza):
    def prepare(self):
        self.dough = self.ingredient_factory.create_dough()
        self.sauce = self.ingredient_factory.create_sauce()
        self.cheese = self.ingredient_factory.create_cheese()
        self.toppings.append(self.ingredient_factory.create_pepperoni())


class PizzaStore:
    def order_pizza(self, item):
        pizza = self.create_pizza(item)
        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()
        return pizza

    # Modified from original HFDP example. This method is shared by subclasses,
    # so concrete classes only need to specify ingredient factory
    def create_pizza(self, item):
        if item == 'cheese':
            pizza = CheesePizza(self.ingredient_factory)
            pizza.name = "New York Style Cheese Pizza"
        elif item == 'pepperoni':
            pizza = PepperoniPizza(self.ingredient_factory)
            pizza.name = "New York Style Pepperoni Pizza"
        else:
            return None
        return pizza


# Concrete PizzaStore classes
class NYPizzaStore(PizzaStore):
    ingredient_factory = NYPizzaIngredientFactory()


class ChicagoPizzaStore(PizzaStore):
    ingredient_factory = ChicagoPizzaIngredientFactory()


def test_pizza_creation_with_ingredient_factory():
    ing_factory = NYPizzaIngredientFactory()
    pizza = CheesePizza(ing_factory)
    pizza.prepare()
    assert pizza.sauce == "MarinaraSauce"
    assert pizza.dough == 'ThinCrustDough'
    ing_factory2 = ChicagoPizzaIngredientFactory()
    pizza2 = CheesePizza(ing_factory2)
    pizza2.prepare()
    assert pizza2.sauce == 'PlumTomatoSauce'
    assert pizza2.dough == 'ThickCrustDough'


def test_create_pizza():
    store = ChicagoPizzaStore()
    pizza = store.create_pizza('pepperoni')
    pizza.prepare()
    assert pizza.sauce == 'PlumTomatoSauce'
    assert 'SlicedPepperoni' in pizza.toppings


def test_order_pizza():
    store = ChicagoPizzaStore()
    pizza = store.order_pizza('pepperoni')
    assert pizza.sauce == 'PlumTomatoSauce'
    assert 'SlicedPepperoni' in pizza.toppings
