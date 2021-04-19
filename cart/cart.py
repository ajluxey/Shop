from django.conf import settings
from decimal import Decimal
from .models import UserCart


class Cart:
    def __init__(self, request, item_class):
        self.session = request.session
        self.item_class = item_class
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_item(self, item, count=1):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = count
        else:
            self.cart[item_id] += count
        self.save()

    def decrease_item_count(self, item):
        self.add_item(item, count=-1)

    def import_item_from_db(self, user_id):
        # user_logged_in() from django.auth.signals
        user_item_count = UserCart.objects.filter(user_id=user_id)
        item_count = user_item_count.values_list('item_id', 'count')
        for item, count in zip(*item_count):
            self.add_item(item, count)
        user_item_count.delete()

    def export_cart_to_db(self, user_id):
        # user_logged_out() from django.auth.signals
        for item_id, count in self.cart.items():
            UserCart.objects.create(user_id=user_id, item_id=int(item_id), count=count)

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def get_total_price(self):
        item_ids = self.cart.keys()
        items = self.item_class.objects.filter(id__in=item_ids)
        return sum(Decimal(item.price) * self.cart[str(item.id)] for item in items)

    def get_items(self):
        item_ids = self.cart.keys()
        return self.item_class.objects.filter(id__in=item_ids)

    def get_id_count(self):
        return self.cart

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def is_empty(self):
        return True if len(self) == 0 else False

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(self.cart.values())


# class Cart:
#     def __init__(self, request, item_class):
#         self.session = request.session
#         self.item_class = item_class
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart
#
#     def add_item(self, item, count=1):
#         item_id = str(item.id)
#         if item_id not in self.cart:
#             self.cart[item_id] = {'count': count,
#                                   'price': str(item.price)}
#         else:
#             self.cart[item_id]['count'] += count
#         self.save()
#         print(self.cart)
#
#     def import_item_from_db(self, user_id):
#         # user_logged_in() from django.auth.signals
#         user_item_count = UserCart.objects.filter(user_id=user_id)
#         item_count = user_item_count.values_list('item_id', 'count')
#         for item, count in zip(*item_count):
#             self.add_item(item, count)
#         user_item_count.delete()
#
#     def export_cart_to_db(self, user_id):
#         # user_logged_out() from django.auth.signals
#         for item_id in self.cart.keys():
#             UserCart.objects.create(user_id=user_id, item_id=item_id, count=self.cart[item_id]['count'])
#
#     def remove(self, item):
#         item_id = str(item.id)
#         if item_id in self.cart:
#             del self.cart[item_id]
#             self.save()
#
#     def get_total_price(self):
#         return sum(Decimal(item['price']) * item['count'] for item in self.cart.values())
#
#     def get_items(self):
#         item_ids = self.cart.keys()
#         return self.item_class.objects.filter(id__in=item_ids)
#
#     def get_id_count(self):
#         return {item_id: self.cart[item_id]['count'] for item_id in self.cart.keys()}
#
#     def clear(self):
#         del self.session[settings.CART_SESSION_ID]
#         self.save()
#
#     def is_empty(self):
#         return True if len(self) == 0 else False
#
#     def save(self):
#         self.session.modified = True
#
#     def __len__(self):
#         return sum(item['count'] for item in self.cart.values())
