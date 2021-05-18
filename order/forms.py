from django import forms
from .models import OrderStatus


class OrderManageForm(forms.Form):
    CHOICES = [(record.status, record.desc) for record in OrderStatus.objects.all()]
    status = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label='Статус заказа')
    message = forms.CharField(max_length=512, required=False, label='Сообщение пользователю')

