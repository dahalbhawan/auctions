from django.contrib.auth.models import AbstractUser
from django.db import models

categories = [
        ("Media", "Media"),
        ("Technology", "Technology"),
        ("Clothing","Clothing"),
        ("Repair","Repair"),
        ("Cleaning","Cleaning"),
        ("Book","Book"),
        ("Household","Household"),
        ("Fashion","Fashion")
    ]

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=categories, blank=True, null=True)
    listed_date = models.DateTimeField(auto_now=True)
    list_price = models.FloatField()
    status = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    image_url = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png")

    def __str__(self):
        return f"{self.id}: {self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, default=None, related_name="listing_bids")
    bid_date = models.DateTimeField(auto_now=True)
    bid_price = models.FloatField()

    def __str__(self):
        return f"{self.id}: {self.bidder.username}"

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Listing, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, default=None, related_name="listing_comments")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"