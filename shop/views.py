from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.
from .models import Item, Brand, Category, Country
from .forms import ItemForm, BrandForm, CategoryForm, CountryForm
from cart.cart import Cart
from .utils import ObjectAddMixin, ObjectDeleteMixin, ObjectUpdateMixin, ObjectsAllMixin


class Catalog(View):
    def get(self, request):
        items = Item.objects.all()
        return render(request, 'shop/catalog.html', context={'items': items, 'items_in_cart': Cart(request).get_items()})


class ItemDetail(View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        in_cart = item in Cart(request).get_items()
        return render(request, 'shop/item.html', context={'item': item, 'in_cart': in_cart})


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.add_item')), name='dispatch')
class ItemAdd(View):
    def get(self, request):
        form = ItemForm()
        return render(request, 'shop/item_add.html', context={'form': form})

    def post(self, request):
        bound_form = ItemForm(request.POST, request.FILES)
        if bound_form.is_valid():
            item = bound_form.save()
            return redirect(item)
        return render(request, 'shop/item_add.html', context={'form': bound_form})


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.change_item')), name='dispatch')
class ItemUpdate(View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        bound_form = ItemForm(instance=item)
        return render(request, 'shop/item_update.html', context={'form': bound_form})

    def post(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        bound_form = ItemForm(request.POST, request.FILES, instance=item)
        if bound_form.is_valid():
            new_item = bound_form.save()
            return redirect(new_item)
        return render(request, 'shop/item_update.html', context={'form': bound_form})


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.delete_item')), name='dispatch')
class ItemDelete(View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        return render(request, 'shop/item_delete.html', context={'item': item})

    def post(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        item.delete()
        return redirect(reverse('catalog'))


class BrandsAll(ObjectsAllMixin, View):
    model = Brand
    template = 'shop/brand/brands_list.html'


class BrandDetail(View):
    def get(self, request, slug):
        brand = get_object_or_404(Brand, slug=slug)
        items = Item.objects.filter(brand=brand)
        return render(request, 'shop/brand/brand.html', context={'brand': brand, 'items': items, 'items_in_cart': Cart(request).get_items()})


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.add_brand')), name='dispatch')
class BrandAdd(ObjectAddMixin, View):
    model = Brand
    template = 'shop/brand/brand_add.html'
    form = BrandForm


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.change_brand')), name='dispatch')
class BrandUpdate(ObjectUpdateMixin, View):
    model = Brand
    template = 'shop/brand/brand_update.html'
    form = BrandForm


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.delete_brand')), name='dispatch')
class BrandDelete(ObjectDeleteMixin, View):
    model = Brand
    template = 'shop/brand/brand_delete.html'


class CategoriesAll(ObjectsAllMixin, View):
    model = Category
    template = 'shop/category/categories_list.html'


class CategoryDetail(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        print(category)
        items = Item.objects.filter(category=category)
        return render(request, 'shop/category/category.html', context={'category': category, 'items': items, 'items_in_cart': Cart(request).get_items()})


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.add_category')), name='dispatch')
class CategoryAdd(ObjectAddMixin, View):
    model = Category
    template = 'shop/category/category_add.html'
    form = CategoryForm


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.change_category')), name='dispatch')
class CategoryUpdate(ObjectUpdateMixin, View):
    model = Category
    template = 'shop/category/category_update.html'
    form = CategoryForm


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.delete_category')), name='dispatch')
class CategoryDelete(ObjectDeleteMixin, View):
    model = Category
    template = 'shop/category/category_delete.html'


class CountriesAll(ObjectsAllMixin, View):
    model = Country
    template = 'shop/country/countries_list.html'


class CountryDetail(View):
    def get(self, request, slug):
        country = get_object_or_404(Country, slug=slug)
        items = Item.objects.filter(country=country)
        return render(request, 'shop/country/country.html', context={'country': country, 'items': items, 'items_in_cart': Cart(request).get_items()})


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.add_country')), name='dispatch')
class CountryAdd(ObjectAddMixin, View):
    model = Country
    template = 'shop/country/country_add.html'
    form = CountryForm


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.change_country')), name='dispatch')
class CountryUpdate(ObjectUpdateMixin, View):
    model = Country
    template = 'shop/country/country_update.html'
    form = CountryForm


@method_decorator(user_passes_test(lambda u: u.has_perm('shop.delete_country')), name='dispatch')
class CountryDelete(ObjectDeleteMixin, View):
    model = Country
    template = 'shop/country/country_delete.html'


class FilteredCatalog(View):
    def get(self, request, filter):
        model_by_name = {'category': Category,
                         'country': Country,
                         'brand': Brand}
        filters = {name: get_object_or_404(model_by_name[name], slug=slug) for name, slug in [filt.split('=') for filt in filter.split('&')]}
        items = Item.objects.filter(**filters).all()
        return render(request, 'shop/catalog.html',
                      context={'items': items,
                               'items_in_cart': Cart(request).get_items()})
