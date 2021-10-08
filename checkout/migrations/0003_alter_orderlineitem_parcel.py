# Generated by Django 3.2.7 on 2021-10-08 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_f_parcel'),
        ('checkout', '0002_remove_order_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='parcel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.parcel'),
        ),
    ]