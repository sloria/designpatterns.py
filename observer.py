'''Observer pattern.
'''

# Modified from HFDP/GOF: No Observer interface defined. Not necessary.
# See comments in http://code.activestate.com/recipes/131499-observer-pattern/


class Subject:

    def __init__(self):
        self.observers = []

    def register_observer(self, obs):
        self.observers.append(obs)

    def remove_observer(self, obs):
        try:
            self.observers.remove(obs)
        except ValueError:
            pass

    def notify_observers(self):
        for each in self.observers:
            each.update()

# Modified from HDFP/GOF: Python allows custom descriptors (can override how a
# property is set and accessed). What a perfect opportunity to notify observers!
class observable_property:
    '''Property that notifies observers when its value changes.

    Gives the property a custom setter which calls the object's ``notify_observers``
    method after the value is set.
    '''
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, type=None):
        value = obj.__dict__.get(self.func.__name__, self.func(obj))
        return value

    def __set__(self, obj, value):
        # Set the value then notify observers
        obj.__dict__[self.func.__name__] = value
        try:
            obj.notify_observers()
        except AttributeError:
            pass


class WeatherData(Subject):

    def __init__(self):
        super().__init__()
        self.__temp = 0.0
        self.__humidity = 0.0
        self.__pressure = 0.0

    # Modified from HFDP/GOF: No need to manually call notify observers manually
    # if using this decorator
    @observable_property
    def temp(self):
        return self.__temp

    @observable_property
    def humidity(self):
        return self.__humidity

    @observable_property
    def pressure(self):
        return self.__pressure

# An Observer
class ConditionsDisplay:
    '''Observes a WeatherData object for changes and displays the current
    conditions every time the weather data changes.
    '''

    def __init__(self, weather_data):
        self.weather_data = weather_data

    def update(self):
        '''Display the current conditions.'''
        # Pull data from weather_data object
        temp, humidity = self.weather_data.temp, self.weather_data.humidity
        print("Current conditions: {temp} deg F and {humidity}% humidity"
                .format(temp=temp, humidity=humidity))


def main():
    data = WeatherData()
    display = ConditionsDisplay(data)
    data.register_observer(display)

    data.temp = 42      # prints "Current conditions: 42 deg F and 0.0% humidity"
    data.humidity = 50  # prints "Current conditions: 42 deg F and 50% humidity"

    data.remove_observer(display)
    data.temp = 31      # Nothing displayed


if __name__ == '__main__':
    main()
