from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    order_notes = models.CharField(max_length=700, blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order number {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name=_('items'))
    product = models.ForeignKey('products.Product',on_delete=models.CASCADE, related_name=_('order_items'))
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'OrderItem {self.id}: {self.product} x {self.quantity} (price: {self.price})'