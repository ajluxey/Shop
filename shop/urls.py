from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('brand/', include([
        path('', BrandsAll.as_view(), name='brands_list'),
        path('add/', BrandAdd.as_view(), name='brand_add'),
        path('<str:slug>/', BrandDetail.as_view(), name='brand_detail'),
        path('<str:slug>/update/', BrandUpdate.as_view(), name='brand_update'),
        path('<str:slug>/delete/', BrandDelete.as_view(), name='brand_delete')
    ])),
    path('category/', include([
        path('', CategoriesAll.as_view(), name='categories_list'),
        path('add/', CategoryAdd.as_view(), name='category_add'),
        path('<str:slug>/', CategoryDetail.as_view(), name='category_detail'),
        path('<str:slug>/update/', CategoryUpdate.as_view(), name='category_update'),
        path('<str:slug>/delete/', CategoryDelete.as_view(), name='category_delete')
    ])),
    path('country/', include([
        path('', CountriesAll.as_view(), name='countries_list'),
        path('add/', CountryAdd.as_view(), name='country_add'),
        path('<str:slug>/', CountryDetail.as_view(), name='country_detail'),
        path('<str:slug>/update/', CountryUpdate.as_view(), name='country_update'),
        path('<str:slug>/delete/', CountryDelete.as_view(), name='country_delete')
    ])),
    path('', Catalog.as_view(), name='catalog'),
    path('add/', ItemAdd.as_view(), name='item_add'),
    path('<str:slug>/', ItemDetail.as_view(), name='item_detail'),
    path('<str:slug>/update/', ItemUpdate.as_view(), name='item_update'),
    path('<str:slug>/delete/', ItemDelete.as_view(), name='item_delete'),
    re_path(r'^filter/(.*=.*&?)+/', FilteredCatalog.as_view(), name='catalog_with_filter')
]
