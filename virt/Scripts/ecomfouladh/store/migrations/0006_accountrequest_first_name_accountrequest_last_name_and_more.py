# Generated by Django 5.0.1 on 2024-05-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_accountrequest_accountdocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountrequest',
            name='first_name',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='accountrequest',
            name='last_name',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='accountrequest',
            name='email',
            field=models.EmailField(default=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='accountrequest',
            name='username',
            field=models.CharField(default=False, max_length=150),
        ),
    ]