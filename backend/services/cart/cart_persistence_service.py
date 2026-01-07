import logging
from repositories.cart_repository import CartRepository
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class CartPersistenceService:
    def __init__(self, cart_repository: CartRepository, product_repository: ProductRepository, user_repository: UserRepository):
        self._cart_repo = cart_repository
        self._product_repo = product_repository
        self._user_repo = user_repository

    def save_cart_state(self, user_id: int) -> None:
        user = self._user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        self._cart_repo.save_user_cart_snapshot(user_id)
        logger.info("Cart state persisted for user %s", user_id)

    def load_cart_state(self, user_id: int):
        user = self._user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        cart_data = self._cart_repo.load_user_cart_snapshot(user_id)
        cart_items = []
        total_price = 0.0
        for entry in cart_data:
            product = self._product_repo.find_by_id(entry["product_id"])
            if product:
                total_price += product.price * entry["quantity"]
                # mimic CartItem return structure
                from models.cart_item import CartItem
                cart_items.append(CartItem(id=0, user_id=user_id, product_id=entry["product_id"], quantity=entry["quantity"], created_at=None, updated_at=None))
        return cart_items, total_price