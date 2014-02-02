"""Adapter pattern

- Converts interface of a class into another interface the client expects.
- Can be useful for adapting legacy code to a newer interface
"""

class WildTurkey:
    def gobble(self):
        return "Gobble gobble"

    def fly(self):
        return "I'm flying a short distance"

class TurkeyAdapter:
    """Adapts a turkey to a duck interface."""
    def __init__(self, turkey):
        self.turkey = turkey

    def quack(self):
        return self.turkey.gobble()

    def fly(self):
        for i in range(5):
            yield self.turkey.fly()

# Alternatively, a generic adapter
# http://ginstrom.com/scribbles/2008/11/06/generic-adapter-class-in-python/
class Adapter(object):
    """Adapts an object by replacing methods.
    Usage:
        dog = Dog()
        dog = Adapter(dog, dict(make_noise=dog.bark))
    """
    def __init__(self, obj, adapted_methods):
        """We set the adapted methods in the object's dict"""
        self.obj = obj
        self.__dict__.update(adapted_methods)
    def __getattr__(self, attr):
        """All non-adapted calls are passed to the object"""
        return getattr(self.obj, attr)

def test_turkey_adapter():
    turkey = WildTurkey()
    adapter = TurkeyAdapter(turkey)
    assert adapter.quack() == 'Gobble gobble'
    assert len(list(adapter.fly())) == 5


def test_generic_adapter():
    turkey = WildTurkey()
    adapter = Adapter(turkey, {"quack": turkey.gobble,
                                "fly": lambda: (turkey.fly() for i in range(5))
                                })
    assert adapter.quack() == 'Gobble gobble'
    assert len(list(adapter.fly())) == 5
