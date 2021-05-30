from django.urls import path, include, re_path
from django.contrib.auth.decorators import permission_required
from .views import *


urlpatterns = [
    path('brand/', include([
        path('', BrandsAll.as_view(), name='brands_list'),
        path('add/', permission_required('shop.add_brand')(BrandAdd.as_view()), name='brand_add'),
        path('<str:slug>/', BrandDetail.as_view(), name='brand_detail'),
        path('<str:slug>/update/', permission_required('shop.change_brand')(BrandUpdate.as_view()), name='brand_update'),
        path('<str:slug>/delete/', permission_required('shop.delete_brand')(BrandDelete.as_view()), name='brand_delete')
    ])),
    path('category/', include([
        path('', CategoriesAll.as_view(), name='categories_list'),
        path('add/', permission_required('shop.add_category')(CategoryAdd.as_view()), name='category_add'),
        path('<str:slug>/', CategoryDetail.as_view(), name='category_detail'),
        path('<str:slug>/update/', permission_required('shop.change_category')(CategoryUpdate.as_view()), name='category_update'),
        path('<str:slug>/delete/', permission_required('shop.delete_category')(CategoryDelete.as_view()), name='category_delete')
    ])),
    path('country/', include([
        path('', CountriesAll.as_view(), name='countries_list'),
        path('add/', permission_required('shop.add_country')(CountryAdd.as_view()), name='country_add'),
        path('<str:slug>/', CountryDetail.as_view(), name='country_detail'),
        path('<str:slug>/update/', permission_required('shop.change_country')(CountryUpdate.as_view()), name='country_update'),
        path('<str:slug>/delete/', permission_required('shop.delete_country')(CountryDelete.as_view()), name='country_delete')
    ])),
    path('', Catalog.as_view(), name='catalog'),
    path('add/', permission_required('shop.add_item')(ItemAdd.as_view()), name='item_add'),
    re_path(r'^filter/$', FilteredCatalog.as_view(), name='catalog_with_filter'),
    path('<str:slug>/', ItemDetail.as_view(), name='item_detail'),
    path('<str:slug>/update/', permission_required('shop.change_item')(ItemUpdate.as_view()), name='item_update'),
    path('<str:slug>/delete/', permission_required('shop.delete_item')(ItemDelete.as_view()), name='item_delete')
]
