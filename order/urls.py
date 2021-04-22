from django.urls import path
from .views import *


urlpatterns = [
    path('', OrderList.as_view(), name='order_list'),
    path('<str:slug>/', OrderDetail.as_view(), name='order_detail')
    ]
