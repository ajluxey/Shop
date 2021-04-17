from django.db import models

# Create your models here.


class UserCart(models.Model):
    user_id = models.PositiveIntegerField()
    item_id = models.PositiveIntegerField()
    count = models.PositiveSmallIntegerField()
