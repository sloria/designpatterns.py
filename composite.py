'''Composite pattern.

- Client treats collection of objects and single objects uniformly
- Trades Single Responsibility principle for *transparency*
    Component has 2 responsibilities: child management and leaf operations
    But client can treat composites and leaves uniformly (whether an element
        is a compositite or leaf is transparent)
'''

class MenuItem:  # A leaf component class
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return "{self.name:30}${self.price:.2f}".format(self=self)

    def display(self):
        print(self)

class Menu:  # the composite component class
    def __init__(self, name):
        self.name = name
        self.components = []  # components may be either menus or items

    def add(self, component):
        self.components.append(component)

    def remove(self, component):
        self.components.remove(component)

    def __str__(self):
        ret = "\n{name}\n".format(name=self.name)
        ret += "-" * 35
        return ret

    def display(self):
        print(self)
        for each in self.components:
            each.display()

def main():
    pancakes = Menu("PANCAKE HOUSE MENU")
    diner = Menu("DINER MENU")
    cafe = Menu("CAFE MENU")
    desserts = Menu("DESSERT MENU")

    all_menus = Menu("ALL MENUS")
    for menu in [pancakes, diner, cafe]:
        all_menus.add(menu)

    # Add menu items
    diner.add(MenuItem("Pasta", 3.89))
    diner.add(MenuItem('BLT', 2.99))
    diner.add(desserts)  # Also add a Menu
    desserts.add(MenuItem("Apple Pie", 1.59))

    pancakes.add(MenuItem('Regular Pancake Breakfast', 2.99))
    pancakes.add(MenuItem('Blueberry Pancakes', 3.49))

    cafe.add(MenuItem('Soup of the day', 3.69))
    cafe.add(MenuItem('Burrito', 4.49))

    # Printing out the composite prints out all components
    all_menus.display()
    # ALL MENUS
    # -----------------------------------

    # PANCAKE HOUSE MENU
    # -----------------------------------
    # Regular Pancake Breakfast     $2.99
    # Blueberry Pancakes            $3.49

    # DINER MENU
    # -----------------------------------
    # Pasta                         $3.89
    # BLT                           $2.99

    # DESSERT MENU
    # -----------------------------------
    # Apple Pie                     $1.59

    # CAFE MENU
    # -----------------------------------
    # Soup of the day               $3.69
    # Burrito                       $4.49


if __name__ == '__main__':
    main()

