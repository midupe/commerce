# Generated by Django 3.0.8 on 2020-07-29 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_main_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='user_id',
            new_name='user',
        ),
    ]
