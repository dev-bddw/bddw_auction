# Generated by Django 3.2.12 on 2022-03-08 16:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='end_time',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lot',
            name='start_time',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
