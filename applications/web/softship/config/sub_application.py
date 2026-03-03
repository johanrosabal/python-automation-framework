from enum import Enum


class SubApplication(Enum):
    MASTER_DATA = "/public/login"
    FINANCE = "/public/login"
    CONTRACT = "/public/login"
    COMMERCIAL = "/public/login"
    CONFIGURATION = "/public/login"
    BOOKING = "/public/login"
    SOF = "/public/login"


class Agencies(Enum):
    CROWLEY_HQ = "Crowley HQ"
