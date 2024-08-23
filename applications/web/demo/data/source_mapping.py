# mapping -> {'Excel Column Name' : 'Object Field Key'}

class UserInformation:

    # Define the mapping fields
    mapping = {
        'username': 'username',
        'email': 'email',
        'typeOfUser': 'type_of_user',
        'enable': 'enable'
    }

    def __init__(self, username, email, type_of_user, enable):
        self.username = username
        self.email = email
        self.type_of_user = type_of_user
        self.enable = bool(enable)

    def __repr__(self):
        return f"UserInformation(username={self.username}, email={self.email}, type_of_user={self.type_of_user}, enable={self.enable})"


class ProductInformation:
    def __init__(self, product_id, name, category, price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price

    def __repr__(self):
        return f"ProductInformation(product_id={self.product_id}, name={self.name}, category={self.category}, price={self.price})"
