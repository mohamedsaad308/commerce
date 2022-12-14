# Generated by Django 4.1 on 2022-09-18 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_listing_categories_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(default='No category', on_delete=django.db.models.deletion.CASCADE, related_name='category_listings', to='auctions.category'),
        ),
    ]
