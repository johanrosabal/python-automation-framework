from enum import Enum


# print(drivers.CHROME.name) => CHROME
# print(drivers.CHROME.value) => chrome
# print(drivers.CHROME.description) => chromedriver.exe


class DriversEnum(Enum):
    CHROME = "chrome", "chromedriver.exe"
    IE = "ie", "IEDriverServer.exe"
    FIRE_FOX = "firefox", "geckodriver.exe"
    EDGE = "edge", "msedge.exe"
    WINDOWS = "Windows", "WindowsPC"

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, description: str = None):
        self._description_ = description

    def __str__(self):
        return self.value

    # this makes sure that the description is read-only
    @property
    def description(self):
        return self._description_
