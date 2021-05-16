from django import forms
from .models import Item, Brand, Country, Category


class FilterForm(forms.Form):
    brands_choices = ((b.slug, b.name) for b in Brand.objects.all())
    category_choices = ((c.slug, c.name) for c in Category.objects.all())
    country_choices = ((c.slug, c.name) for c in Country.objects.all())

    brand = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                      choices=brands_choices,
                                      required=False,
                                      label='Производители')
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                         choices=category_choices,
                                         required=False,
                                         label='Категории')
    country = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                        choices=country_choices,
                                        required=False,
                                        label='Страны')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'desc', 'price', 'count', 'brand', 'country', 'category', 'img']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # 'img': forms.ImageField(attrs={'class': 'form-control'})
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'desc']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control'})
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'desc']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control'})
        }


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
