from django.urls import path
from .views import *


urlpatterns = [
    path('', OrderList.as_view(), name='order_list'),
    path('management', OrderManagementList.as_view(), name='order_management'),
    path('<str:slug>/', OrderDetail.as_view(), name='order_detail'),
    path('<str:slug>/manage', OrderDetailManage.as_view(), name='order_detail_management')
    ]
