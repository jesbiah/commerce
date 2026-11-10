from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)
    image_url = models.CharField(max_length=256)

    def __str__(self):
        return f'Category: {self.name}'


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)

    # There should be a way to get current price
    starting_bid = models.IntegerField()
    image_url = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')

    def __str__(self):
        return f'{self.title} ({self.category})'


class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name='watchers')


class Bid(models.Model):
    amount = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='bids')

    def __str__(self):
        return f'$ {self.amount} for {self.listing} by {self.user}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=256)

    def __str__(self):
        return f'"{self.title}" - {self.listing} by {self.user}'

