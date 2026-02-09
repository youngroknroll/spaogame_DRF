"""
Orders 도메인 비즈니스 로직

Service Layer는 비즈니스 규칙과 트랜잭션 경계를 담당합니다.
View는 HTTP 처리만, Service는 도메인 로직만 담당합니다.
"""

import logging

from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.products.models import DetailedProduct, Product

from .models import Cart, CartItem, Wishlist, WishlistItem

logger = logging.getLogger(__name__)


class CartService:
    """장바구니 비즈니스 로직"""

    @staticmethod
    @transaction.atomic
    def add_item(user, product_id=None, detailed_product_id=None, quantity=1):
        """
        장바구니에 상품 추가

        Args:
            user: 사용자 객체
            product_id: 상품 ID (선택)
            detailed_product_id: 상세상품 ID (선택)
            quantity: 수량 (기본 1)

        Returns:
            CartItem: 생성 또는 업데이트된 장바구니 항목
        """
        logger.info(
            f"장바구니 추가 시도: user={user.email}, "
            f"product_id={product_id}, detailed_product_id={detailed_product_id}, "
            f"quantity={quantity}"
        )

        cart, _ = Cart.objects.get_or_create(user=user)

        if detailed_product_id:
            detailed_product = get_object_or_404(DetailedProduct, id=detailed_product_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, detailed_product=detailed_product, defaults={"quantity": quantity}
            )
        else:
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, defaults={"quantity": quantity}
            )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        logger.info(
            f"장바구니 추가 완료: cart_item_id={cart_item.id}, "
            f"created={created}, final_quantity={cart_item.quantity}"
        )

        return cart_item

    @staticmethod
    @transaction.atomic
    def update_item_quantity(user, item_id, quantity):
        """
        장바구니 항목 수량 변경

        Args:
            user: 사용자 객체
            item_id: CartItem ID
            quantity: 새로운 수량

        Returns:
            CartItem: 업데이트된 장바구니 항목
        """
        logger.info(
            f"장바구니 수량 변경: user={user.email}, item_id={item_id}, quantity={quantity}"
        )

        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=user)
        cart_item.quantity = quantity
        cart_item.save()

        logger.info(f"장바구니 수량 변경 완료: cart_item_id={cart_item.id}")

        return cart_item

    @staticmethod
    @transaction.atomic
    def remove_item(user, item_id):
        """
        장바구니 항목 삭제

        Args:
            user: 사용자 객체
            item_id: CartItem ID
        """
        logger.info(f"장바구니 항목 삭제: user={user.email}, item_id={item_id}")

        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=user)
        cart_item.delete()

        logger.info(f"장바구니 항목 삭제 완료: item_id={item_id}")


class WishlistService:
    """위시리스트 비즈니스 로직"""

    @staticmethod
    @transaction.atomic
    def add_item(user, product_id):
        """
        위시리스트에 상품 추가

        Args:
            user: 사용자 객체
            product_id: 상품 ID

        Returns:
            tuple: (WishlistItem, created)
        """
        logger.info(f"위시리스트 추가: user={user.email}, product_id={product_id}")

        product = get_object_or_404(Product, id=product_id)
        wishlist, _ = Wishlist.objects.get_or_create(user=user)

        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist, product=product
        )

        logger.info(f"위시리스트 추가 완료: wishlist_item_id={wishlist_item.id}, created={created}")

        return wishlist_item, created

    @staticmethod
    @transaction.atomic
    def remove_item(user, item_id):
        """
        위시리스트 항목 삭제

        Args:
            user: 사용자 객체
            item_id: WishlistItem ID
        """
        logger.info(f"위시리스트 삭제: user={user.email}, item_id={item_id}")

        wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=user)
        wishlist_item.delete()

        logger.info(f"위시리스트 삭제 완료: item_id={item_id}")
