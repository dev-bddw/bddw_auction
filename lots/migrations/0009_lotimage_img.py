# Generated by Django 3.2.12 on 2022-03-15 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0008_lotimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotimage',
            name='img',
            field=models.ImageField(default=None, null=True, upload_to='lots'),
        ),
    ]