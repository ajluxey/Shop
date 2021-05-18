from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views.generic import View
from .models import Order
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from shop.models import Item
from .models import OrderStatus
from .forms import OrderManageForm
# Create your views here.


# TODO: сделать нормальный слаг, потому что он вставляет id до создания
@method_decorator(user_passes_test(lambda u: u.has_perm('order.view_order')), name='dispatch')
class OrderList(View):
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id).order_by('-created_at').all()
        return render(request, 'order/order_list.html', context={'orders': orders})


@method_decorator(user_passes_test(lambda u: u.has_perm('order.view_order')), name='dispatch')
class OrderDetail(View):
    def get(self, request, slug):
        order = get_object_or_404(Order, slug=slug)
        if order.user != request.user and not request.user.groups.filter(name='Manager').exists():
            return HttpResponseForbidden()
        items = order.items.all()
        oic = order.orderitemcount_set.all()
        id_count = dict(oic.values_list('item_id', 'count'))
        return render(request, 'order/order_detail.html', context={'order': order,
                                                                   'items': items,
                                                                   'id_count': id_count})

    # TODO: сделать возврат товара на склад, но нужно ли?
    def post(self, request, slug):
        order = get_object_or_404(Order, slug=slug)
        order.status = OrderStatus.objects.get(status='CANCELED')
        order.save()
        return redirect('order_list')


class OrderManagementList(View):
    def get(self, request):
        orders = Order.objects.order_by('-created_at').all()
        return render(request, 'order/order_list_manage.html', context={'orders': orders})


class OrderDetailManage(View):
    def get(self, request, slug):
        order = get_object_or_404(Order, slug=slug)
        items = order.items.all()
        oic = order.orderitemcount_set.all()
        id_count = dict(oic.values_list('item_id', 'count'))
        form = OrderManageForm({'status': order.status.status})
        return render(request, 'order/order_detail_manage.html', context={'order': order,
                                                                          'items': items,
                                                                          'id_count': id_count,
                                                                          'form': form})

    def post(self, request, slug):
        form = OrderManageForm(request.POST)
        if not form.changed_data:
            return redirect('order_management')
        if form.is_valid():
            order = Order.objects.get(slug=slug)
            if 'status' in form.changed_data:
                status = OrderStatus.objects.get(status=form.data['status'])
                order.status = status
            if 'message' in form.changed_data:
                order.mes2usr = form.data['message']
            order.save()
        return redirect('order_management')

