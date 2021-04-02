from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View

# Create your views here.
from .models import Item
from .forms import ItemForm


class Catalog(View):
    def get(self, request):
        items = Item.objects.all()
        return render(request, 'shop/catalog.html', context={'items': items})


class ItemDetail(View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        return render(request, 'shop/item.html', context={'item': item})


class ItemAdd(View):
    def get(self, request):
        form = ItemForm()
        return render(request, 'shop/item_add.html', context={'form': form})

    def post(self, request):
        bound_form = ItemForm(request.POST)
        if bound_form.is_valid():
            item = bound_form.save()
            redirect(item)
        return render(request, 'shop/item_add.html', context={'form': bound_form})


class ItemUpdate(View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        bound_form = ItemForm(instance=item)
        return render(request, 'shop/item_update.html', context={'form': bound_form})

    def post(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        bound_form = ItemForm(request.POST, instance=item)
        if bound_form.is_valid():
            new_item = bound_form.save()
            redirect(new_item)
        return render(request, 'shop/item_update.html', context={'form': bound_form})


class ItemDelete(View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        return render(request, 'shop/item_delete.html', context={'item': item})

    def post(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        item.delete()
        return redirect(reverse('catalog'))
