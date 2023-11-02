from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


from .models import *


# shows when there is an empty route
def index(request):
    # show listings that are active in the index page
    active_listings = Listing.objects.filter(is_active=True)
    
    # this is for index view purpose to let user choose a category
    all_categories = Category.objects.all()

    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories
    })



# opens a web page for user to make listing
def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })
    elif request.method == "POST":
        # Get the data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        price_value = int(request.POST["price"])  # Convert the price to an integer
        category_name = request.POST["category"]

        # Who is the user
        current_user = request.user

        # Get the category based on the category name
        category = Category.objects.get(category_name=category_name)

        # Create a new bid for the price
        price_bid = Bid(bid=price_value, user=current_user)
        price_bid.save()  # Save the bid to the database

        # Create a new listing object and assign the price_bid
        new_listing = Listing(
            title=title,
            description=description,
            image_url=image_url,
            price=price_bid,  # Assign the created Bid instance
            owner=current_user,
            category=category
        )

        new_listing.save()  # Save the new listing to the database

        # Redirect to the index page
        return HttpResponseRedirect(reverse(index))




"""
shows the listings of the particular category after that the user chooses, 
redirect to index page having the listings of that particular category.
"""
def display_category(request):
    if request.method == "POST":
        user_selected_category = request.POST['category']
        category = Category.objects.get(category_name=user_selected_category)
        
        # all active listings of the category that user chooses
        active_listings = Listing.objects.filter(is_active=True, category=category)

        all_categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": active_listings,
            "categories": all_categories
        })
        



"""
shows new web called 'lisitng' page that enables user for placing bids, see more description, making comments
"""

def listing_page(request, id):

    # stores all listing data
    listing_data = Listing.objects.get(pk=id)

    # stores bool value weather the user is in the wathclist of the listing
    is_in_watchlist = request.user in listing_data.watchlist.all()

    # stores all comments; Comment is a django model
    all_comments = Comment.objects.all()

    # stores the bool value: checks weather current listing is created by the current user or not 
    is_owner = request.user.username == listing_data.owner.username

    return render(request, "auctions/listing_page.html", {
        "listing": listing_data,
        "is_in_watchlist": is_in_watchlist,
        "comments": all_comments,
        "is_owner": is_owner
    })




def remove_from_watchlist(request, id):

    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.remove(current_user)

    return HttpResponseRedirect(reverse("listing_page", args=(id, )))




def add_to_watchlist(request, id):

    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.add(current_user)

    return HttpResponseRedirect(reverse("listing_page", args=(id, )))




 
"""
shows all the listings that a user put into watchlist by oneself 
"""
def watchlist(reqeust):
    current_user = reqeust.user
    # here 'listing' is a related name to watchlist in the model
    listings = current_user.listing.all()
    return render(reqeust, "auctions/watchlist.html", {
        "listings": listings
    })





def add_comment(request, id):
    current_user = request.user
    listing_data = Listing.objects.get(pk=id)
    user_comment = request.POST['add_comment']

    new_comment = Comment(
        author=current_user,
        listing=listing_data,
        comment=user_comment
    )

    new_comment.save()
    
    return HttpResponseRedirect(reverse("listing_page", args=(id, )))



def add_bid(request, id):

    new_bid = request.POST['add_bid']
    listing_data = Listing.objects.get(pk=id)
    is_in_watchlist = request.user in listing_data.watchlist.all()
    all_comments = Comment.objects.all()

    if int(new_bid) > listing_data.price.bid:
        update_bid = Bid(user=request.user, bid=int(new_bid))
        update_bid.save()
        listing_data.price = update_bid
        listing_data.save()
        return render(request, "auctions/listing_page.html", {
            "listing": listing_data,
            "message": "Bid Updated Successful",
            "update": True,
            "is_in_watchlist": is_in_watchlist,
            "comments": all_comments
        })
    
    else:
        return render(request, "auctions/listing_page.html", {
            "listing": listing_data,
            "message": "Bid Updated Failed",
            "update": False,
            "is_in_watchlist": is_in_watchlist,
            "comments": all_comments
        })





def close_auction(request, id):

    listing_data = Listing.objects.get(pk=id)
    listing_data.is_active = False
    listing_data.save()
    is_owner = request.user.username == listing_data.owner.username
    is_in_watchlist = request.user in listing_data.watchlist.all()
    all_comments = Comment.objects.all()

    return render(request, "auctions/listing_page.html", {
        "listing": listing_data,
        "is_in_watchlist": is_in_watchlist,
        "comments": all_comments,
        "is_owner": is_owner,
        "update": True,
        "message": "Congratulation! Your auction is closed."
    })



"""
def login_view
def logout_view
class CustomUserCreationForm
def register
"""



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




# Create a custom registration form that requires 4 values
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Check that all fields are filled
        if not (username and email and password1 and password2):
            raise forms.ValidationError("All fields are required.")

        return cleaned_data




# Register view which takes 'form' from the above class
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError as e:
                logger.error(f"Error creating user: {e}")
        else:
            logger.error("Form is not valid")
    else:
        form = CustomUserCreationForm()

    return render(request, "auctions/register.html", {"form": form})