from django.conf import settings
from decimal import Decimal
from .models import UserCart
from shop.models import Item


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.item_class = Item
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

    def import_cart_from_db(self, user_id):
        user_item_count = UserCart.objects.filter(user_id=user_id)
        item_count = user_item_count.values_list('item_id', 'count')
        for item_id, count in item_count:
            print(item_id, count)
            self.add_item(self.item_class.objects.filter(id=item_id).get(), count)
        user_item_count.delete()

    def export_cart_to_db(self, user_id):
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
        return {int(item_id): count for item_id, count in self.cart.items()}

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def is_empty(self):
        return True if len(self) == 0 else False

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(self.cart.values())
