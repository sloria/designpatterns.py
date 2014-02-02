"""Iterator pattern.

- Encapsulate iteration to allow traversal without exposing the underlying
    implementation
"""

# Two menu collections with different internal representations
class PancakeMenu:

    def __init__(self):
        # Stores menu items and prices in 2 lists
        self.items = []
        self.prices = []

    def __getitem__(self, key):
        '''Get the price of an item.'''
        return self.prices[self.items.index(key)]

    def add_item(self, item, price):
        self.items.append(item)
        self.prices.append(price)

    def __iter__(self):
        return iter(zip(self.items, self.prices))  # Iterator is built into Python

class DinerMenu:

    def __init__(self):
        # Stores menu items and prices in a dict
        self.menu_items = {}

    def __getitem__(self, key):
        '''Get the price of an item.'''
        return self.menu_items[key]

    def add_item(self, item, price):
        self.menu_items[item] = price

    def __iter__(self):
        return iter(self.menu_items.items())

def print_full_menu(*menus):
    # unified interface for traversing elements
    for menu in menus:
        for item, price in menu:
            print("{item:30}${price:.2f}".format(item=item, price=price))


def main():
    pancakes = PancakeMenu()
    pancakes.add_item("Buttermilk pancakes", 3.0)
    pancakes.add_item("Blueberry pancakes", 4.5)
    diner_menu = DinerMenu()
    diner_menu.add_item("BBQ Ribs", 6.0)
    diner_menu.add_item("Fish and chips", 5.0)
    print_full_menu(pancakes, diner_menu)

if __name__ == '__main__':
    main()
