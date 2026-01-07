import logging
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class CartQuantityService:
    def __init__(self, cart_repository: CartRepository, product_repository: ProductRepository) -> None:
        self._cart_repo = cart_repository
        self._product_repo = product_repository

    def update_quantity(self, user_id: int | None, product_id: int, quantity: int) -> float:
        logger.info("Updating product %s in user %s cart to quantity %s", product_id, user_id, quantity)
        if quantity is None or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        cart_item = self._cart_repo.find_cart_item(user_id, product_id)
        if not cart_item:
            raise ValueError("Product not found in cart.")
        self._cart_repo.update_quantity(cart_item.id, quantity)
        return self._calculate_total(user_id)

    def _calculate_total(self, user_id: int | None) -> float:
        items = self._cart_repo.get_user_cart_items(user_id)
        total = 0.0
        for item in items:
            product = self._product_repo.find_by_id(item.product_id)
            if product:
                total += product.price * item.quantity
        logger.info("Recalculated total price: %.2f", total)
        return total