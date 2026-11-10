from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Listing, User


# THERE HAS TO BE A STREAMLINED WAY TO MAKE A FORM FROM A MODEL
class NewListingForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    starting_bid = forms.IntegerField()
    image_url = forms.CharField(max_length=256)
    # category = forms.ForeignKey(AuctionCategory, related_name='listings')


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings,
    })


def create_listing(request):
    
    # Check if POST
    if request.method == 'POST':

        # Validate form
        form = NewListingForm(request.POST)
        if form.is_valid():

            # Save form data--AGAIN THERE HAS TO BE A STREAMLINED WAY

            # Redirect to new listing
            return HttpResponseRedirect(reverse('listing')) #, args=(,)

    # Else render template
    return render(request, 'auctions/create.html')


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