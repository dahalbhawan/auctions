# Generated by Django 3.1.1 on 2021-02-16 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_comment_date_created'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Auction',
            new_name='Listing',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='auction',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='auction',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_bids', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_comments', to='auctions.listing'),
        ),
    ]
