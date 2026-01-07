import logging
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class CartRemovalService:
    def __init__(self, cart_repository: CartRepository, product_repository: ProductRepository) -> None:
        self._cart_repo = cart_repository
        self._product_repo = product_repository

    def remove_product_from_cart(self, user_id: int | None, product_id: int) -> float:
        logger.info("Removing product %s from cart of user %s", product_id, user_id)
        cart_item = self._cart_repo.find_cart_item(user_id, product_id)
        if not cart_item:
            raise ValueError("Product not found in cart.")
        product = self._product_repo.find_by_id(product_id)
        if not product:
            raise ValueError("Product information unavailable for total recalculation.")
        self._cart_repo.delete_item(cart_item.id)
        updated_total = self._calculate_total(user_id)
        logger.info("Product removed successfully. Updated total: %.2f", updated_total)
        return updated_total

    def _calculate_total(self, user_id: int | None) -> float:
        items = self._cart_repo.get_user_cart_items(user_id)
        total = 0.0
        for item in items:
            product = self._product_repo.find_by_id(item.product_id)
            if product:
                total += product.price * item.quantity
        return total