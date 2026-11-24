from django.contrib.auth.models import User
from django.db import models
from django.db.models.constraints import UniqueConstraint


# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    model = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    horsepower = models.PositiveIntegerField()
    release_date = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    body_type = models.CharField(max_length=50)
    length = models.PositiveIntegerField(default=0, null=True, blank=True)
    width = models.PositiveIntegerField(default=0, null=True, blank=True)
    height = models.PositiveIntegerField(default=0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    colors_available = models.CharField(max_length=250)
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField()


    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.brand} {self.model}'


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    pfp = models.ImageField(upload_to='profile_pics/', default='static/cardealership/images/default.jpg')
    location = models.CharField(max_length=100, null=True, blank=True)
    contact_info = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Comment(models.Model):
    listing = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # prevents a user from favoriting a car twice
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'car'],
                name='unique_favorite'
            )
        ]