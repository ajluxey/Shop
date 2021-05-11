from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.urls import get_resolver

from .utils import translit


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=128, unique=True)    #, default='Без названия')
    desc = models.CharField(max_length=512, db_index=True)  #, default='Нет описания')
    slug = models.SlugField(max_length=150, unique=True)    #, default='-')

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})

    @staticmethod
    def slug_gen(name):
        return slug_gen_for(Brand, name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.slug_gen(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Brand: {self.name}'


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)    #, default='Без названия')
    desc = models.CharField(max_length=512, db_index=True)  #, default='Нет описания')
    slug = models.SlugField(max_length=150, unique=True)    #, default='-')

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    @staticmethod
    def slug_gen(name):
        return slug_gen_for(Category, name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.slug_gen(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Category: {self.name}'


class Country(models.Model):
    name = models.CharField(max_length=128, unique=True)    #, default='Без названия')
    slug = models.SlugField(max_length=150, unique=True)    #, default='-')

    def get_absolute_url(self):
        return reverse('country_detail', kwargs={'slug': self.slug})

    @staticmethod
    def slug_gen(name):
        return slug_gen_for(Country, name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.slug_gen(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Country: {self.name}'


class Item(models.Model):
    name = models.CharField(max_length=128, unique=True, db_index=True)
    desc = models.CharField(max_length=512, db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.PositiveSmallIntegerField()
    # img = models.ImageField(upload_to=, blank=True)
    # оценка товара
    # s_of_r8 = models.IntegerField()
    # c_of_r8 = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='items', blank=True)
    category = models.ManyToManyField('Category', related_name='items', blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='items', blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'slug': self.slug})

    @staticmethod
    def slug_gen(name):
        return slug_gen_for(Item, name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.slug_gen(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Item: {self.name}'


def slug_gen_for(model, name):
    slug = slugify(translit(name))
    # TODO: проверка на зарезервированные имена
    # reserved_urls = get_resolver().reverse_dict.keys()
    # reserved_urls = [url for url in reserved_urls if isinstance(url, str)]
    try:
        slug_already_exist = model.objects.get(slug=slug)
    except model.DoesNotExist:
        slug_already_exist = None
    if slug_already_exist:  # or slug in reserve_urls:
        from time import time
        slug += str(time())
    return slug