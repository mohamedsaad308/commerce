# Generated by Django 4.1 on 2022-08-31 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_listing_image'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watchlist',
            unique_together=set(),
        ),
    ]