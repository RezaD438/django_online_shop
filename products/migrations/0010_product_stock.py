# Generated by Django 4.1.7 on 2023-05-09 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
