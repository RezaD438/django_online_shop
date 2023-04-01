# Generated by Django 4.1.7 on 2023-04-01 03:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_datetime_created_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='datetime_created_test',
        ),
        migrations.AlterField(
            model_name='product',
            name='datetime_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date Time of Creation'),
        ),
    ]
