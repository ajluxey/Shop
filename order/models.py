from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from shop.utils import translit
from users.models import CustomUser
# Create your models here.


class OrderStatus(models.Model):
    DEFAULT_STATUS_ID = 1
    # Status list
    # (IN_PROGRESS, 'Обрабатывается'),
    # (PAYMENT_EXPECTED, 'Ожидается оплата'),
    # (ACCEPTED, 'Заказ принят'),
    # (READY_FOR_DELIVERY, 'Готов к выдаче'),
    # (RECEIVED, 'Получен'),
    # (CANCELED, 'Отклонён')
    status = models.CharField(max_length=64, unique=True)
    desc = models.CharField(max_length=64)


class Order(models.Model):
    # user_id = models.PositiveIntegerField()
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True)
    mes2usr = models.CharField(max_length=512, blank=True)
    items = models.ManyToManyField('shop.Item', through='OrderItemCount')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='order', blank=True,
                               verbose_name='Статус', default=OrderStatus.DEFAULT_STATUS_ID)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'slug': self.slug})

    def slug_gen(self):
        user = self.user

        from datetime import datetime
        now = datetime.now()
        now = now.strftime('%H%M%S%d%m%Y')

        slug = user.first_name[0] + user.last_name[0] + str(self.user.id) + now
        slug = slugify(translit(slug))

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

    class Meta:
        ordering = ['-created_at']


class OrderItemCount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey('shop.Item', on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField()
