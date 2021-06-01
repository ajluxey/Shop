from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import QueryDict


# Create your views here.
from .models import Item, Brand, Category, Country
from .forms import ItemForm, BrandForm, CategoryForm, CountryForm, FilterForm
from cart.cart import Cart
from .utils import ObjectAddMixin, ObjectDeleteMixin, ObjectUpdateMixin, ObjectsAllMixin, \
    filter_str_by_form, get_params_about_page

from functools import reduce
from operator import iand


# TODO: сделать отображение страны, категорий и производителя


class Catalog(View):
    def get(self, request):
        form = FilterForm()
        items = Item.objects.all()

        paginator = Paginator(items, 9)
        page = paginator.get_page(request.GET.get('page', 1))
        is_paginated, prev_url, next_url = get_params_about_page(page)
        context = {'page': page,
                   'items_in_cart': Cart(request).get_items(),
                   'form': form,
                   'is_paginated': is_paginated,
                   'prev_url': prev_url,
                   'next_url': next_url,
                   'base_query': '?'}

        return render(request, 'shop/catalog.html', context=context)

    def post(self, request):
        form = FilterForm(request.POST)
        if not form.changed_data:
            return redirect('catalog')

        if form.is_valid():
            return redirect(reverse('catalog_with_filter') + '?' + filter_str_by_form(form))
        else:
            return redirect('catalog')


class FilteredCatalog(View):
    def get(self, request):
        model_by_name = {'category': Category,
                         'country': Country,
                         'brand': Brand}

        filters = {}
        form_data = QueryDict('', mutable=True)
        for filter_category, filter_model in model_by_name.items():
            slugs = request.GET.get(filter_category)
            if slugs:
                slugs = slugs.split(',')
                form_data.setlist(filter_category, slugs)
                objects = filter_model.objects.filter(slug__in=slugs)

                for obj in objects:
                    q = Q(**{filter_category: obj})
                    if filter_category in filters:
                        filters[filter_category] |= q
                    else:
                        filters[filter_category] = q

        form = FilterForm(form_data)
        items = Item.objects.filter(reduce(iand, filters.values())).all()
        paginator = Paginator(items, 9)
        page = paginator.get_page(request.GET.get('page', 1))
        base_query = '?' + filter_str_by_form(form)
        is_paginated, prev_url, next_url = get_params_about_page(page, base_query=base_query)
        context = {'page': page,
                   'items_in_cart': Cart(request).get_items(),
                   'form': form,
                   'is_paginated': is_paginated,
                   'prev_url': prev_url,
                   'next_url': next_url,
                   'base_query': base_query + '&'}

        return render(request, 'shop/catalog.html', context=context)

    def post(self, request):
        form = FilterForm(request.POST)
        if not form.changed_data:
            return redirect('catalog')

        if form.is_valid():
            return redirect(reverse('catalog_with_filter') + '?' + filter_str_by_form(form))
        else:
            return redirect('catalog')


class ItemDetail(View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        in_cart = item in Cart(request).get_items()
        return render(request, 'shop/item.html', context={'item': item, 'in_cart': in_cart})


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
    verbose_name = 'Производители'
    mess_if_empty = 'У нас нет сведений по производителям'


class BrandDetail(View):
    def get(self, request, slug):
        brand = get_object_or_404(Brand, slug=slug)
        items = Item.objects.filter(brand=brand)
        paginator = Paginator(items, 9)
        page = paginator.get_page(request.GET.get('page', 1))
        is_paginated, prev_url, next_url = get_params_about_page(page)
        context = {'brand': brand,
                   'page': page,
                   'items_in_cart': Cart(request).get_items(),
                   'is_paginated': is_paginated,
                   'prev_url': prev_url,
                   'next_url': next_url,
                   'base_query': '?'}
        return render(request, 'shop/brand/brand.html', context=context)


class BrandAdd(ObjectAddMixin, View):
    model = Brand
    template = 'shop/brand/brand_add.html'
    form = BrandForm


class BrandUpdate(ObjectUpdateMixin, View):
    model = Brand
    template = 'shop/brand/brand_update.html'
    form = BrandForm


class BrandDelete(ObjectDeleteMixin, View):
    model = Brand
    template = 'shop/brand/brand_delete.html'
    redirect_on_delete = 'brands_list'


class CategoriesAll(ObjectsAllMixin, View):
    model = Category
    template = 'shop/category/categories_list.html'
    verbose_name = 'Категории'
    mess_if_empty = 'У нас нет сведений о категориях'


class CategoryDetail(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        items = Item.objects.filter(category=category)
        paginator = Paginator(items, 9)
        page = paginator.get_page(request.GET.get('page', 1))
        is_paginated, prev_url, next_url = get_params_about_page(page)
        context = {'category': category,
                   'page': page,
                   'items_in_cart': Cart(request).get_items(),
                   'is_paginated': is_paginated,
                   'prev_url': prev_url,
                   'next_url': next_url,
                   'base_query': '?'}
        return render(request, 'shop/category/category.html', context=context)


class CategoryAdd(ObjectAddMixin, View):
    model = Category
    template = 'shop/category/category_add.html'
    form = CategoryForm


class CategoryUpdate(ObjectUpdateMixin, View):
    model = Category
    template = 'shop/category/category_update.html'
    form = CategoryForm


class CategoryDelete(ObjectDeleteMixin, View):
    model = Category
    template = 'shop/category/category_delete.html'
    redirect_on_delete = 'categories_list'


class CountriesAll(ObjectsAllMixin, View):
    model = Country
    template = 'shop/country/countries_list.html'
    verbose_name = 'Страны'
    mess_if_empty = 'У нас нет сведений о странах'


class CountryDetail(View):
    def get(self, request, slug):
        country = get_object_or_404(Country, slug=slug)
        items = Item.objects.filter(country=country)
        paginator = Paginator(items, 9)
        page = paginator.get_page(request.GET.get('page', 1))
        is_paginated, prev_url, next_url = get_params_about_page(page)
        context = {'country': country,
                   'page': page,
                   'items_in_cart': Cart(request).get_items(),
                   'is_paginated': is_paginated,
                   'prev_url': prev_url,
                   'next_url': next_url,
                   'base_query': '?'}
        return render(request, 'shop/country/country.html', context=context)


class CountryAdd(ObjectAddMixin, View):
    model = Country
    template = 'shop/country/country_add.html'
    form = CountryForm


class CountryUpdate(ObjectUpdateMixin, View):
    model = Country
    template = 'shop/country/country_update.html'
    form = CountryForm


class CountryDelete(ObjectDeleteMixin, View):
    model = Country
    template = 'shop/country/country_delete.html'
    redirect_on_delete = 'countries_list'
