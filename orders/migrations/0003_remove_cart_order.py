# Generated by Django 3.2.12 on 2022-03-19 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20220317_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='order',
        ),
    ]
