from django.urls import path
from django.contrib.auth.decorators import permission_required
from .views import *


urlpatterns = [
    path('', permission_required('order.view_order')(OrderList.as_view()), name='order_list'),
    path('management', permission_required('order.change_order')(OrderManagementList.as_view()), name='order_management'),
    path('<str:slug>/', permission_required('order.view_order')(OrderDetail.as_view()), name='order_detail'),
    path('<str:slug>/manage', permission_required('order.change_order')(OrderDetailManage.as_view()), name='order_detail_management')
    ]
