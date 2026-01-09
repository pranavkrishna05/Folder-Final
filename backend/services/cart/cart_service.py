import logging
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from models.cart_item import CartItem

logger = logging.getLogger(__name__)

class CartService:
    def __init__(self, cart_repository: CartRepository, product_repository: ProductRepository) -> None:
        self._cart_repo = cart_repository
        self._product_repo = product_repository

    def add_product_to_cart(self, user_id: int | None, product_id: int, quantity: int) -> CartItem:
        logger.info("Attempting to add product %s to cart for user %s", product_id, user_id)
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        product = self._product_repo.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found or unavailable.")
        existing_item = self._cart_repo.find_existing_item(user_id, product_id)
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            self._cart_repo.update_quantity(existing_item.cart_id, new_quantity)
            logger.info("Updated quantity for product %s in cart.", product_id)
            existing_item.quantity = new_quantity
            return existing_item
        return self._cart_repo.add_item(user_id, product_id, quantity)

    def clear_cart_after_logout(self, user_id: int):
        logger.info("Clearing cart for user ID %s after logout", user_id)
        self._cart_repo.clear_user_cart(user_id)
        logger.info("Cart cleared for user ID %s", user_id)