# Generated by Django 5.0.1 on 2024-05-10 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_order1_orderitem_shippingaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order1',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
    ]
