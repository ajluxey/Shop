from django.urls import path
from .views import *


urlpatterns = [
    path('', Catalog.as_view(), name='catalog'),
    path('brand/', BrandsAll.as_view(), name='brands_list'),
    path('category/', CategoriesAll.as_view(), name='categories_list'),
    path('country/', CountriesAll.as_view(), name='countries_list'),
    path('add/', ItemAdd.as_view(), name='item_add'),
    path('<str:slug>/', ItemDetail.as_view(), name='item_detail'),
    path('<str:slug>/update', ItemUpdate.as_view(), name='item_update'),
    path('<str:slug>/delete', ItemDelete.as_view(), name='item_delete'),
    path('brand/add/', BrandAdd.as_view(), name='brand_add'),
    path('brand/<str:slug>/', BrandDetail.as_view(), name='brand_detail'),
    path('brand/<str:slug>/update', BrandUpdate.as_view(), name='brand_update'),
    path('brand/<str:slug>/delete', BrandDelete.as_view(), name='brand_delete'),
    path('category/add/', CategoryAdd.as_view(), name='category_add'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_detail'),
    path('category/<str:slug>/update', CategoryUpdate.as_view(), name='category_update'),
    path('category/<str:slug>/delete', CategoryDelete.as_view(), name='category_delete'),
    path('country/add/', CountryAdd.as_view(), name='country_add'),
    path('country/<str:slug>/', CountryDetail.as_view(), name='country_detail'),
    path('country/<str:slug>/update', CountryUpdate.as_view(), name='country_update'),
    path('country/<str:slug>/delete', CountryDelete.as_view(), name='country_delete')
]
