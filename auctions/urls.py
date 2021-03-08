from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all-listings/", views.closed_listings_view, name="closed_listings"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("add/", views.add_listing, name="add"),
    path("watchlist/", views.watchlist_view, name='watchlist'),
    path("add-to-watchlist/<int:item_id>/", views.add_to_watchlist_view, name='add_to_watchlist'),
    path("remove-from-watchlist/<int:item_id>/", views.remove_from_watchlist_view, name='remove_from_watchlist'),
    path('categories/', views.category_list_view, name="category_list"),
    path('category/<str:category>/', views.category_view, name='category'),
    path("listing/<int:listing_id>/", views.listing_view, name="listing"),
    path("close-bid/<int:item_id>/", views.close_bid_view, name="close_bid"),
    path("add-comment/<int:item_id>/", views.add_comment_view, name="add_comment"),
]
