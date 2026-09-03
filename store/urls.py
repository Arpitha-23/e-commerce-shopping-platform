from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.order_history, name='order_history'),
    path(
    'wishlist/add/<int:product_id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'
),
path(
    'wishlist/',
    views.wishlist,
    name='wishlist'
),
path(
    'wishlist/remove/<int:product_id>/',
    views.remove_from_wishlist,
    name='remove_from_wishlist'
),
path(
    'create-razorpay-order/',
    views.create_razorpay_order,
    name='create_razorpay_order'
),
path(
    'verify-razorpay-payment/',
    views.verify_razorpay_payment,
    name='verify_razorpay_payment'
),
]