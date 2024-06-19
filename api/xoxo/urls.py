from django.urls import path
from .views import get_vouchers, get_Order, place_order

urlpatterns = [
    path('vouchers/', get_vouchers, name='get_vouchers'),
    path('vouchers/order/',get_Order, name='get_order' ),
    path('vouchers/order/<int:productid>', place_order, name="post_order"),
]
