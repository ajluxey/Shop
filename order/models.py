from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from shop.utils import translit
from users.models import CustomUser
# Create your models here.


class Order(models.Model):
    user_id = models.PositiveIntegerField()
    slug = models.SlugField(max_length=150, unique=True)
    items = models.ManyToManyField('shop.Item', through='OrderItemCount')

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'slug': self.slug})

    def slug_gen(self):
        user = CustomUser.objects.get(id=self.user_id)
        slug = user.first_name[0] + user.last_name[0] + str(self.id)
        slug = slugify(translit(slug))
        # TODO: проверка на зарезервированные имена
        # reserved_urls = get_resolver().reverse_dict.keys()
        # reserved_urls = [url for url in reserved_urls if isinstance(url, str)]
        try:
            slug_already_exist = Order.objects.get(slug=slug)
        except Order.DoesNotExist:
            slug_already_exist = None
        if slug_already_exist:  # or slug in reserve_urls:
            from time import time
            slug += str(time())
        return slug

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.slug_gen()
        super().save(*args, **kwargs)


class OrderItemCount(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.ForeignKey('shop.Item', on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField()
