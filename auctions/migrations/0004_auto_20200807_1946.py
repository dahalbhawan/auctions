# Generated by Django 3.0.8 on 2020-08-07 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(blank=True, choices=[('Media', 'Media'), ('Clothing', 'Clothing'), ('Repair', 'Repair'), ('Cleaning', 'Cleaning'), ('Book', 'Book'), ('Household', 'Household'), ('Fashion', 'Fashion')], max_length=20),
        ),
    ]
