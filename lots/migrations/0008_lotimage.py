# Generated by Django 3.2.12 on 2022-03-15 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0007_auto_20220315_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='LotImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
