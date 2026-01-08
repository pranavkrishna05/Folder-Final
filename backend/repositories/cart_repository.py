import logging
from datetime import datetime
from models.cart_item import CartItem

class CartRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def add_item_to_cart(self, user_id: int, item: CartItem):
        existing_item = self.find_existing_item(user_id, item.product.id)
        if existing_item:
            existing_item.quantity += item.quantity
            existing_item.last_updated = datetime.now()
            self.db_session.update(existing_item)
        else:
            item.last_updated = datetime.now()
            self.db_session.add(item)
        self.db_session.commit()

    def find_existing_item(self, user_id: int, product_id: int):
        # Simulating a query to find an existing cart item for the user
        for item in self.db_session.query(CartItem).filter_by(user_id=user_id, product_id=product_id):
            return item
        return None
