from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator


def translit(string):
    tr_alph = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sc', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'iu', 'я': 'ia', 'ё': 'e'}
    new_s = ''
    for char in string.lower():
        if char in tr_alph:
            char = tr_alph[char]
        new_s += char
    return new_s


def get_params_about_page(page, base_query=''):
    is_paginated = page.has_other_pages()
    symbol = '&' if base_query else '?'
    prev_url = base_query + f'{symbol}page={page.previous_page_number()}' if page.has_previous() else ''
    next_url = base_query + f'{symbol}page={page.next_page_number()}' if page.has_next() else ''
    return is_paginated, prev_url, next_url


def filter_str_by_form(form):
    filter_names = ['brand', 'category', 'country']
    filter_ = []
    for name in filter_names:
        values = form.data.getlist(name)
        if values:
            values_str = ','.join(values)
            filter_.append(f'{name}={values_str}')
    return '&'.join(filter_)


class ObjectAddMixin:
    model = None
    template = None
    form = None

    def get(self, request):
        form = self.form()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form(request.POST)
        if bound_form.is_valid():
            brand = bound_form.save()
            return redirect(brand)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    template = None
    form = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        bound_form = self.form(instance=obj)
        return render(request, self.template, context={'form': bound_form})

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        bound_form = self.form(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_on_delete = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        return render(request, self.template, context={'obj': obj})

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        obj.delete()
        return redirect(reverse(self.redirect_on_delete))


class ObjectsAllMixin:
    model = None
    template = None
    verbose_name = None
    mess_if_empty = None

    def get(self, request):
        objects = self.model.objects.all()
        paginator = Paginator(objects, 9)
        page = paginator.get_page(request.GET.get('page', 1))
        is_paginated, prev_url, next_url = get_params_about_page(page)
        context = {'page': page,
                   'is_paginated': is_paginated,
                   'prev_url': prev_url,
                   'next_url': next_url,
                   'base_query': '?',
                   'verbose_name': self.verbose_name,
                   'mess_if_empty': self.mess_if_empty}
        return render(request, self.template, context=context)



