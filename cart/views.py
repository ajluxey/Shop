from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .cart import Cart
from shop.models import Item
# Create your views here.


class CartDetail(View):
    def get(self, request):
        cart = Cart(request)
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
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.add_item(item)
    return redirect('cart_detail')


def decrease_item_count(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.decrease_item_count(item)
    return redirect('cart_detail')


def remove_from_cart(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart_detail')


def get_cart_json(request):
    return JsonResponse(Cart(request).get_id_count())


def get_total_price(request):
    return JsonResponse({'total_price': Cart(request).get_total_price()})


@receiver(user_logged_in)
def extend_cart_from_db(sender, user, request, **kwargs):
    Cart(request).import_cart_from_db(user.id)


@receiver(user_logged_out)
def send_cart_to_db(sender, user, request, **kwargs):
    Cart(request).export_cart_to_db(user.id)
