# Generated by Django 3.0.8 on 2020-07-30 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200729_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='main_img',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]