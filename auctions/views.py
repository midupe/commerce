from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import os, os.path

from .models import *


def index(request, message=""):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings, "message": message})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def rename_uploaded_file(filename, id):
    extension = os.path.splitext(filename)[1]
    renamedfile = str(id) + extension
    os.rename(r'media/images/%s' % filename, r'media/images/%s' % renamedfile)
    return renamedfile

@login_required
def create_listing(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["desc"]
        category = request.POST["category"]
        main_img = None
        if 'img' in request.FILES:  
            main_img = request.FILES["img"]

        starting_bid = request.POST["starting_bid"]
        user = get_user(request)

        if category == "null" or None:
            category = None
        else:
            category = Category.objects.get(name=category)
        #create listing
        listing = Listing.objects.create(user =user, category=category, name=title, main_img=main_img, desc=desc, starting_bid=starting_bid)
        if listing is not None:
            listing.save()
            id = listing.id
            if main_img is not None:
                rename = rename_uploaded_file(main_img.name, id)
                Listing.objects.filter(id=id).update(main_img=("images/"+rename))
            return render(request, "auctions/create.html", {"categories": categories, "message": "Created successfully"})
        else:
            return render(request, "auctions/create.html", {"categories": categories, "message": "Something went wrong"})


    return render(request, "auctions/create.html", {"categories": categories})

def updatebids():
    listings = Listing.objects.all()
    bids = Bid.objects.all()

    for listing in listings:
        for bid in bids:
            if listing.id == bid.listing_id:
                if listing.last_bid is None or listing.last_bid < bid.value:
                    Listing.objects.filter(id=listing.id).update(last_bid=bid.value)

def listing(request, id):
    message = ""
    bid_is_current_bid = 0
    try:
        listing = Listing.objects.get(id=id)
    except:
        return index(request, message="Listing number " + str(id) + " doesn't exist!")
    else:
        listing_user = User.objects.get(id=listing.user_id)
        if request.method == "POST":
            if 'watchlist' in request.POST:
                if Watchlist.objects.filter(listing_id = listing, user_id=get_user(request)):
                    #remove
                    Watchlist.objects.filter(listing_id = listing, user_id=get_user(request)).delete()
                else:
                    #add to watchlist
                    a = Watchlist.objects.create(user_id=get_user(request), listing = listing)
                    a.save()
            if 'makebid' in request.POST:
                bid = float(request.POST["bid"])
                if listing.last_bid is not None:
                    if bid > float(listing.last_bid):
                        b = Bid.objects.create(value=bid ,user_id=get_user(request), listing = listing)
                        b.save()
                        updatebids()
                        message = "Bid created"
                    else:
                        message = "Invalid Bid"
                else:
                    if float(listing.starting_bid) < bid:
                        b = Bid.objects.create(value=bid, user_id=get_user(request), listing = listing)
                        b.save()
                        updatebids()
                        message = "Bid created"
                    else:
                        message = "Invalid Bid"

        listing = Listing.objects.get(id=id)

        if request.user.is_authenticated:
            username = request.user.username
            numBids = len(Bid.objects.filter(listing_id=listing))
            if len(Bid.objects.filter(listing_id=listing, value=listing.last_bid , user_id=get_user(request))) > 0  :
                bid_is_current_bid = 1
            return render(request, "auctions/listing.html", {"username": username,"listing": listing, "numBids": numBids, "message": message, "listing_user": listing_user, "bid_is_current_bid": bid_is_current_bid})
        else:
            return render(request, "auctions/listing.html", {"listing": listing, "message": message, "listing_user": listing_user, "bid_is_current_bid": bid_is_current_bid})

def watchlist(request):
    user = get_user(request)
    watchlist = Watchlist.objects.filter(user_id = user)
    listings = Listing.objects.all()
    favourites = []
    for i in watchlist:
        for j in listings:
            if j.id == i.listing_id:
                favourites.append(j)
    return render(request, "auctions/watchlist.html", {"listings": favourites})

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/category-list.html", {"categories": categories})

def category(request, id):
    if id == "undefined":
        id =None
    categories = Category.objects.all()
    listings = Listing.objects.filter(category_id=id)
    return render(request, "auctions/category.html", {"categories": categories, "listings": listings})