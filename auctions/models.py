from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone

class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=50, unique=True)
    

class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey('User', related_name='owner', on_delete=models.CASCADE,)
    category = models.ForeignKey('Category', null = True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    main_img = models.ImageField(upload_to=('images/'), null=True)
    desc = models.CharField(max_length=200)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    last_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_created = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')
    status = models.CharField(max_length=50, default='activated')
    winner = models.ForeignKey('User', related_name='winner', on_delete=models.SET_NULL, null = True)


class Bid(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE) 
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE,) 
    value = models.DecimalField(max_digits=10, decimal_places=2)

class Comment(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE) 
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE,)
    text = models.TextField()
    date_created =  models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')


class Watchlist(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE,)