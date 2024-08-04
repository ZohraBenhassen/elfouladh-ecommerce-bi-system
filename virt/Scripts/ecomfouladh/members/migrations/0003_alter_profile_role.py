# Generated by Django 5.0.1 on 2024-06-22 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_alter_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('sdvente', 'Sales'), ('dirgen', 'Director General'), ('livreur', 'Delivery')], max_length=10),
        ),
    ]