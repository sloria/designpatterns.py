'''Strategy Pattern

- Behavior delegation
- Program to an interface rather than an implementation
- Composition > Inheritance

Unlike the original example in Java, there's no need to create a
base strategy interface since Python supports higher-order functions.
'''

### Behaviors ####

# Modified from HDFP/GOF: behaviors are functions instead of classes.
# These functions are injected into objects upon instantiation.

def quack():
    return "Quack"

def mute_quack():
    return "<< Silence >>"

def squeak():
    return "squeak"

def fly_with_wings():
    return "I'm flying!"

def fly_no_way():
    return "I can't fly"

### Duck classes ###

class Duck:

    def __init__(self):
        self.quack_behavior = None
        self.fly_behavior = None

    # Varying behaviors are delegated
    def fly(self):
        return self.fly_behavior()

    def quack(self):
        return self.quack_behavior()

    # A non-varying behavior
    def swim(self):
        return 'All ducks float, even decoys!'


class MallardDuck(Duck):

    def __init__(self):
        self.quack_behavior = quack
        self.fly_behavior = fly_with_wings

def test():
    mallard = MallardDuck()
    assert mallard.quack() == 'Quack'
    assert mallard.fly()  == "I'm flying!"
    assert mallard.swim() == 'All ducks float, even decoys!'
    # Can change behaviors at runtime
    mallard.quack_behavior = mute_quack
    assert mallard.quack() == '<< Silence >>'

if __name__ == '__main__':
    test()
