# Generated by Django 3.2.7 on 2021-11-02 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_userprofile_default_street_full_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='default_street_full_name',
            new_name='default_full_name',
        ),
    ]