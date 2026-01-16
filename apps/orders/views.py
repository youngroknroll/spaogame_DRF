"""
Orders 앱 뷰 (FBV 방식)
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.products.models import Product


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_list(request):
    """
    장바구니 조회 및 상품 추가
    - GET: 장바구니 조회 (없으면 빈 장바구니 반환)
    - POST: 장바구니에 상품 추가
    """
    if request.method == 'GET':
        cart = Cart.objects.filter(user=request.user).first()
        
        if not cart:
            # 장바구니가 없으면 빈 응답 반환
            return Response({"id": None, "items": [], "created_at": None, "updated_at": None})
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # 장바구니 조회 또는 생성
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        # 상품 조회
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {"error": "수량은 정수여야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if quantity <= 0:
            return Response(
                {"error": "수량은 1 이상이어야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "상품을 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 장바구니에 상품 추가 또는 수량 업데이트
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # 이미 존재하면 수량 누적
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_item_detail(request, item_id):
    """
    장바구니 항목 수정 및 삭제
    - PATCH: 수량 변경
    - DELETE: 항목 제거
    """
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    except CartItem.DoesNotExist:
        return Response(
            {"error": "장바구니 항목을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'PATCH':
        # 수량 변경
        quantity = request.data.get('quantity')
        if quantity is None:
            return Response(
                {"error": "수량이 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {"error": "수량은 정수여야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if quantity <= 0:
            return Response(
                {"error": "수량은 1 이상이어야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        # 항목 제거
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
