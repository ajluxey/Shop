from django.urls import path
from .views import *


urlpatterns = [
    path('', Catalog.as_view(), name='catalog'),
    path('add/', ItemAdd.as_view(), name='item_add'),
    path('<str:slug>/', ItemDetail.as_view(), name='item_detail'),
    path('<str:slug>/update', ItemUpdate.as_view(), name='item_update'),
    path('<str:slug>/delete', ItemDelete.as_view(), name='item_delete')
]
