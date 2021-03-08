# Generated by Django 3.1.1 on 2021-02-12 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210211_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(blank=True, choices=[('Media', 'Media'), ('Technology', 'Technology'), ('Clothing', 'Clothing'), ('Repair', 'Repair'), ('Cleaning', 'Cleaning'), ('Book', 'Book'), ('Household', 'Household'), ('Fashion', 'Fashion')], max_length=20, null=True),
        ),
    ]
