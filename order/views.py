from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Order, OrderItemCount
from shop.models import Item
# Create your views here.


# TODO: сделать нормальный слаг, потому что он вставляет id до создания
class OrderList(View):
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id).all()
        return render(request, 'order/order_list.html', context={'orders': orders})


class OrderDetail(View):
    def get(self, request, slug):
        order = get_object_or_404(Order, slug=slug)
        items = order.items.all()
        oic = order.orderitemcount_set.all()
        id_count = dict(oic.values_list('item_id', 'count'))
        return render(request, 'order/order_detail.html', context={'order': order,
                                                                   'items': items,
                                                                   'id_count': id_count})

    # TODO: сделать возврат товара на склад, но нужно ли?
    def post(self, request, slug):
        order = get_object_or_404(Order, slug=slug)
        order.delete()
        return redirect('order_list')
