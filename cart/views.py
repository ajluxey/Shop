from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from .cart import Cart
from shop.models import Item
# Create your views here.


class CartDetail(View):
    def get(self, request):
        cart = Cart(request, Item)
        items = cart.get_items()
        # print(items.values_list('id'))
        id_count = cart.get_id_count()
        # print(id_count)
        total_price = cart.get_total_price()
        return render(request, 'cart/cart_detail.html', context={'items': items,
                                                                 'id_count': id_count,
                                                                 'total_price': total_price})

    def post(self, request):    # оформление заказа
        pass


def add_to_cart(request, item_id):
    cart = Cart(request, Item)
    item = get_object_or_404(Item, id=item_id)
    cart.add_item(item)
    return redirect('cart')


def remove_from_cart(request, item_id):
    cart = Cart(request, Item)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart')


def cart_detail_json(request):
    pass
