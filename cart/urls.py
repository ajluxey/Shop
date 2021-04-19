from django.urls import path
from .views import *


urlpatterns = [
    path('', CartDetail.as_view(), name='cart_detail'),
    path('add/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('decrease/<int:item_id>', decrease_item_count, name='decrease_item_count'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('get_json/', get_cart_json, name='cart_json'),
    path('get_total_price/', get_total_price, name='total_price')
    ]
