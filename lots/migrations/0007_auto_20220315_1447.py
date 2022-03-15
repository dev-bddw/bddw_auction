# Generated by Django 3.2.12 on 2022-03-15 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0006_lot_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='lot',
            name='img',
            field=models.ImageField(default=None, null=True, upload_to='lots'),
        ),
        migrations.AddField(
            model_name='lot',
            name='name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='lot',
            name='sku',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
