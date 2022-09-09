from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import Category, User, Listing, Watchlist, Bid, Comment, Watchlist
from .forms import CategoryForm, ListingForm

def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {"listings": listings})


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

@login_required
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

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = ListingForm()

    return render(request, 'auctions/add-listing.html', {'form': form})  


def show_listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    comments = listing.listing_comments.all()
    context = {"listing" : listing}
    context['comments'] = comments
    last_bid = listing.listing_bids.order_by('-bid_value').first()
    if last_bid:
        context['last_bid_value'] = last_bid.bid_value
        context['winner'] = last_bid.user
    else:
        context['winner'] = listing.user
    return render(request, 'auctions/listing.html', context)

@login_required
def edit_watchlist(request, id):
    listing = Watchlist.objects.filter(listing_id = id, user_id=request.user.id)
    if listing:
        listing.delete()
    else:
        listing = Watchlist(listing_id = id, user_id=request.user.id)
        listing.save()
    return redirect('show-listing', id)

    

@login_required
def create_bid(request, id):
    if request.method == "POST":
        current_bid_value = int(request.POST["bid"])
        last_bid = Bid.objects.filter(listing_id=id).order_by('-bid_value').first()
        if last_bid:
            if current_bid_value <= last_bid.bid_value:
                request.session["message"] = f"Your bid shoud be greater than the last bid (${last_bid.bid_value})"
                return redirect('show-listing', id) 
        else:
            listing = get_object_or_404(Listing, id=id)
            if listing:
                if current_bid_value < listing.price:
                    request.session["message"] = f"Your bid shoud be equal or greater than the starting bid (${listing.price})"
                    return redirect('show-listing', id)

        bid = Bid(bid_value=current_bid_value, listing_id=id, user=request.user)
        bid.save()
        request.session.pop("message", None)
    return redirect('show-listing', id)  

@login_required
def close_auction(request, id):
    listing = get_object_or_404(Listing, id=id)
    listing.active = False
    listing.save()
    return redirect('show-listing', id)

@login_required
def create_comment(request, id):
    if request.method == "POST":
        text = request.POST['comment']
        comment = Comment(text=text, user=request.user, listing_id=id)
        comment.save()
        return redirect('show-listing', id)

@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    listings = []
    for w in watchlist:
        listings.append(w.listing)

    return render(request, "auctions/watchlist.html", {"listings": listings})

def categories(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')

    else:
        form = CategoryForm()

    return render(request, 'auctions/categories.html', {"form": form, "categories":categories})

def category_listings(request, id):
    context = {}
    category = Category.objects.get(id = id).name
    context["category"] = category
    listings = Listing.objects.filter(category_id=id, active=True)
    context['listings'] = listings
    return render(request, 'auctions/category-listings.html', context)