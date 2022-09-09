from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add-listing", views.add_listing, name="add-listing"),
    path("listing/<int:id>", views.show_listing, name="show-listing"),
    path("listing/<int:id>/watchlist", views.edit_watchlist, name="edit-watchlist"),
    path("listing/<int:id>/create-bid", views.create_bid, name="create-bid"),
    path("listing/<int:id>/close-auction", views.close_auction, name="close-auction"),
    path("listing/<int:id>/comment", views.create_comment, name="create-comment"),
    path("user/watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>/listings", views.category_listings, name="category-listings"),
]
