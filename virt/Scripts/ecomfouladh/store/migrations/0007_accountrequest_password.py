# Generated by Django 5.0.1 on 2024-05-20 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_accountrequest_first_name_accountrequest_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountrequest',
            name='password',
            field=models.CharField(default=False, max_length=50),
        ),
    ]
