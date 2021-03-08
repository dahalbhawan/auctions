from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ListingForm, BidForm, CommentForm
from django.db.models import Max, Count

from .models import User, Listing, Bid, categories, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(status=True),
        "heading": "Active Listings"
    })

def closed_listings_view(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(status=False),
        "heading": "Closed Listings"
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
            messages.error(request, "Invalid username or password.")
            return render(request, "auctions/login.html", {
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
            watchlist = Watchlist.objects.create(user=user)
            watchlist.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "auctions/register.html", {
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def add_listing(request):
    form = ListingForm()
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            list_price = form.cleaned_data['list_price']
            image_url = form.cleaned_data['image_url']
            listing = Listing.objects.create(title=title,
                                             description=description,
                                             category=category,
                                             list_price=list_price,
                                             image_url=image_url,
                                             author=request.user)
            listing.save()
            messages.success(request, "Listing created successfully")
            return HttpResponseRedirect(reverse('index'))
        return render(request, "auctions/add.html", {
            'from': form
        })
    return render(request, "auctions/add.html", {
        'form': form
    })

def listing_view(request, listing_id):
    form = BidForm()
    comment_form = CommentForm()
    listing = Listing.objects.get(pk=listing_id)
    last_bid = listing.listing_bids.last()
    if not last_bid:
        last_bid = Bid(bidder=listing.author, listing=listing, bid_price=listing.list_price)
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_price = form.cleaned_data['bid_price']
            if bid_price > last_bid.bid_price:
                bid = Bid.objects.create(bidder=request.user,
                                         listing=listing,
                                         bid_price=bid_price)
                bid.save()
                messages.success(request, "You have successfully placed your bid.")
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            messages.error(request, "Bid price must be greater than current bid price.")
            return render(request, "auctions/listing.html", {
                "form": form,
                "listing": listing,
                "bid_count": listing.listing_bids.count(),
                "last_bid": last_bid,
                "comment_form": comment_form,
            })
        return render(request, "auctions/listing.html", {
            "form": form,
            "listing": listing,
            "bid_count": listing.listing_bids.count(),
            "last_bid": last_bid,
            "comment_form": comment_form,
        })
    return render(request, "auctions/listing.html", {
        "form": form,
        "listing": listing,
        "bid_count": listing.listing_bids.count(),
        "last_bid": last_bid,
        "comment_form": comment_form,
    })

def category_list_view(request):
    category_counts = []
    all_categories = [category[0] for category in categories]
    for category in all_categories:
        category_counts.append((category, Listing.objects.filter(category=category, status=True).count()))
    return render(request, 'auctions/categories.html', {
        'category_counts': category_counts,
    })

def category_view(request, category):
    listings = Listing.objects.filter(category=category, status=True)
    return render(request, 'auctions/index.html', {
        'listings': listings,
        'category': category,
    })

@login_required(login_url='login')
def add_to_watchlist_view(request, item_id):
    listing = Listing.objects.get(pk=item_id)
    watchlist = Watchlist.objects.get(user=request.user)
    if request.method == "POST":
        watchlist.items.add(listing)
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing.pk}))

@login_required(login_url='login')
def watchlist_view(request):
    user = request.user
    watchlist_items = user.watchlist.items.all()
    return render(request, 'auctions/watchlist.html', {
        'listings': watchlist_items
    })

@login_required(login_url='login')
def remove_from_watchlist_view(request, item_id):
    watchlist = Watchlist.objects.get(user=request.user)
    listing = Listing.objects.get(pk=item_id)
    if request.method == 'POST':
        watchlist.items.remove(listing)
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def close_bid_view(request, item_id):
    listing = Listing.objects.get(pk=item_id)
    user = request.user
    if request.method == 'POST':
        listing.status = False
        listing.save()
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': item_id}))

@login_required(login_url='login')
def add_comment_view(request, item_id):
    user = request.user
    listing = Listing.objects.get(pk=item_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = user
        comment.listing = listing
        comment.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": item_id}))