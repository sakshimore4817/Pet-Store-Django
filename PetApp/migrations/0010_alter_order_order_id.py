# Generated by Django 5.0 on 2024-01-10 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PetApp', '0009_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
