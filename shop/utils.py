from django.shortcuts import render, get_object_or_404, redirect, reverse


def translit(string):
    tr_alph = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sc', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'iu', 'я': 'ia', 'ё': 'e'}
    new_s = ''
    for char in string.lower():
        if char in tr_alph:
            char = tr_alph[char]
        new_s += char
    return new_s


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

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        return render(request, self.template, context={'obj': obj})

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        obj.delete()
        return redirect(reverse('catalog'))


class ObjectsAllMixin:
    model = None
    template = None

    def get(self, request):
        objects = self.model.objects.all()
        return render(request, self.template, context={'objects': objects})
