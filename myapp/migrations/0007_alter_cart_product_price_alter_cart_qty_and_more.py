# Generated by Django 5.0.2 on 2024-08-02 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_cart_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='cart',
            name='qty',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.PositiveIntegerField(),
        ),
    ]
