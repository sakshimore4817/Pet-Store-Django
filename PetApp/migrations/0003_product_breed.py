# Generated by Django 5.0 on 2023-12-14 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PetApp', '0002_product_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='breed',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
