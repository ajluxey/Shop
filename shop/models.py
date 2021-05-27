from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.urls import get_resolver

from .utils import translit


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название')
    desc = models.CharField(max_length=512, db_index=True, verbose_name='Описание')
    slug = models.SlugField(max_length=150, unique=True)
    # updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название')
    desc = models.CharField(max_length=512, db_index=True, verbose_name='Описание')
    slug = models.SlugField(max_length=150, unique=True)
    # updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True)
    # updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        ordering = ['name']


class Item(models.Model):
    name = models.CharField(max_length=128, unique=True, db_index=True, verbose_name='Название')
    desc = models.CharField(max_length=512, db_index=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    count = models.PositiveSmallIntegerField(verbose_name='Количество')
    img = models.ImageField(upload_to='images/items', blank=True, verbose_name='Фото товара')
    # оценка товара
    # s_of_r8 = models.IntegerField()
    # c_of_r8 = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='items', blank=True, verbose_name='Производитель')
    category = models.ManyToManyField('Category', related_name='items', blank=True, verbose_name='Категории')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='items', blank=True, verbose_name='Страна производитель')
    slug = models.SlugField(max_length=150, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        ordering = ['-updated_at']


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