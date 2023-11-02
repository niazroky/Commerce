from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# create category models to store category data
class Category(models.Model):
    category_name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.category_name



# user place bids, now bid is a djanog model
class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

    def __str__(self) -> str:
        return f"{self.bid}"


"""
Create Listing models to store listing data. It has various types
of data. A category may have many listings but a listing can have
only one category. 
"""
class Listing(models.Model):
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=250)
    image_url = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="from_user_bid")
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listing")

    def __str__(self) -> str:
        return self.title
    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comment")
    comment = models.CharField(max_length=150)

    def __str__(self):
        return f"-{self.author}"