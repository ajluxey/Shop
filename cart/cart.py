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

    def add_item(self, item, count=1, update_quantity=False):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'count': count,
                                  'price': str(item.price)}
        if update_quantity:
            self.cart[item_id]['count'] += count
        self.save()

    def import_item_from_db(self, user_id):
        user_item_count = UserCart.objects.filter(user_id=user_id)
        item_ids, counts = user_item_count.values('item_id', 'count')       # ? че каво
        items = self.item_class.objects.filter(id__in=item_ids)
        for item, count in zip(items, counts):
            self.add_item(item, count)
        user_item_count.delete()

    def export_cart_to_db(self, user_id):
        for item_id in self.cart.keys():
            UserCart.objects.create(user_id=user_id, item_id=item_id, count=self.cart[item_id]['count'])

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['count'] for item in self.cart.values())

    def get_items(self):
        item_ids = self.cart.keys()
        return self.item_class.objects.filter(id__in=item_ids)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def is_empty(self):
        return True if len(self) == 0 else False

    def save(self):
        self.session.modified = True

    # def __iter__(self):         # нужен ли вообще итератор?
    #     item_ids = self.cart.keys()
    #     items = self.item_class.objects.filter(id__in=item_ids)
    #     cart = self.cart.copy()
    #     for item in items:                      # нужно ли?
    #         cart[str(item.id)]['item'] = item   # вот это
    #     for item in cart.values():
    #         item['price'] = Decimal(item['price'])
    #         item['total_price'] = item['price'] * item['count']
    #         yield item

    def __len__(self):
        return sum(item['count'] for item in self.cart.values())
