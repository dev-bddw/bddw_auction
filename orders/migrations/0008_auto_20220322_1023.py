# Generated by Django 3.2.12 on 2022-03-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='checkout_session_id',
            new_name='stripe_checkout_session_id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='json_event_obj',
            new_name='stripe_json_event_obj',
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_message',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
