from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])


# custom comment manager
class ActiveCommentsManger(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentsManger, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', '1 star'),
        ('2', '2 star'),
        ('3', '3 star'),
        ('4', '4 star'),
        ('5', '5 star'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name="Comment Text")
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name="what is your score")

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    # custom comment manager
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManger()

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])
