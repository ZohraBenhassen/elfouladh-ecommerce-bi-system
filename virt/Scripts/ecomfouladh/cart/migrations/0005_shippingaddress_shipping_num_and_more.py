# Generated by Django 5.0.1 on 2024-06-23 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_shippingaddress_shipping_address2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='shipping_num',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_email',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
