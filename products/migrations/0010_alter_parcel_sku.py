# Generated by Django 3.2.7 on 2021-11-10 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_parcel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='sku',
            field=models.CharField(max_length=254, null=True),
        ),
    ]