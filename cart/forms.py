from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)] # TODO: сделать подгрузку товара из корзины

# class CartAddProductForm(forms.Form):
#     count =