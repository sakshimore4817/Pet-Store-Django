# Generated by Django 5.0 on 2024-01-04 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PetApp', '0006_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imag1',
            field=models.ImageField(null=True, upload_to='media'),
        ),
        migrations.AddField(
            model_name='product',
            name='imag2',
            field=models.ImageField(null=True, upload_to='media'),
        ),
        migrations.AddField(
            model_name='product',
            name='imag3',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
