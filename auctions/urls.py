from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add-category", views.add_category, name="add-category"),
    path("add-listing", views.add_listing, name="add-listing"),
    path("listing/<int:id>", views.show_listing, name="show-listing"),
    path("watchlist/<int:id>", views.edit_watchlist, name="edit-watchlist"),
]
