from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('logout', logout_user, name="logout_user"),
    path('option/', option_of_trading, name="option_of_trading"),
    path('addBid/', add_product_for_bid, name="add_product_for_bid"),
    path('addBid/sell_your_product', sell_product, name="sell_product"),
    path('deals/', show_all_products, name="show_all_products"),
    path('deals/order', view_Orders, name="view_Orders"),
    path('buy_product/<str:product_id>/', buy_product, name="buy_product"),
    path('send_mail/', send_mail_Test, name='send_mail_Test'),
    path('deals/notification/', wishlist, name='wishlist'),
    path('deals/wishlist/<str:product_id>/', added_wishlist, name="added_wishlist"),
    path('proceed to payment', payment_and_post_buy, name="payment_and_post_buy"),
]
