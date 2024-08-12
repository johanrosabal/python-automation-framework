from dataclasses import dataclass

"""
dataclasses
added to Python 3.7 (and later backported to Python 3.6)

created using a @dataclass decorator

by default add automatically generated dunder methods __init__, __repr__ and __eq__ 
__init__ method takes all fields as method parameters and sets their values to instance attributes with the same names:
"""


@dataclass
class UserDTO:
    user_name: str
    user_password: str
