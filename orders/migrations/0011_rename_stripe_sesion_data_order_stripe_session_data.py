# Generated by Django 3.2.12 on 2022-03-22 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20220322_1233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='stripe_sesion_data',
            new_name='stripe_session_data',
        ),
    ]
