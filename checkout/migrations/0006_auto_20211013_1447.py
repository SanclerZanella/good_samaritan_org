# Generated by Django 3.2.7 on 2021-10-13 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_rename_original_bag_orderlineitem_original_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlineitem',
            name='original_cart',
        ),
        migrations.RemoveField(
            model_name='orderlineitem',
            name='stripe_pid',
        ),
        migrations.AddField(
            model_name='order',
            name='original_cart',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_pid',
            field=models.CharField(default='', max_length=254),
        ),
    ]
