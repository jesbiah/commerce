from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Category, Listing, User


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
    

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings,
    })


def category(request, category_name):
    category = Category.objects.get(name=category_name)
    return render(request, 'auctions/category.html', {
        'category': category
    })


def categories(request):
    return render(request, 'auctions/categories.html', {
        'categories': Category.objects.all()
    })


def create(request):
    
    # Check if POST
    if request.method == 'POST':

        # Validate form
        form = ListingForm(request.POST)
        if form.is_valid():

            # Save form data
            form.save()

            # Redirect to new listing
            return HttpResponseRedirect(reverse('listing')) #, args=(,)
        else:
            message = 'Invalid entry'
            return render(request, 'auctions/create.html', {
                'form': form,
                'message': message
            })

    # Else render template
    return render(request, 'auctions/create.html', {
        'form': ListingForm()
    })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, 'autions/listing.html', {
        'listing': listing
    })


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


def unwatch(request):
    pass


def watch(request):
    pass


def watchlist(request):
    if request.user.is_authenticated:

        # Show watchlist page
        return render(request, 'auctions/watchlist.html')

    # Else, redirect to login page
    return HttpResponseRedirect(reverse('login'))