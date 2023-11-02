from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("display_category", views.display_category, name="display_category"),
    path("listing_page/<int:id>", views.listing_page, name="listing_page"),
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("add_bid/<int:id>", views.add_bid, name="add_bid"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction")
]
