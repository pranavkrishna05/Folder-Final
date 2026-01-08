from datetime import datetime
from models.product import Product

class CartItem:
    def __init__(self, product: Product, quantity: int, last_updated: datetime = None):
        self.product = product
        self.quantity = quantity
        self.last_updated = datetime.now() if last_updated is None else last_updated

    def update_quantity(self, new_quantity: int):
        self.quantity = new_quantity
        self.last_updated = datetime.now()

