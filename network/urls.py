
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create", views.create, name="create"),
    path("save", views.save, name="save"),
    path("postapi/<int:postid>", views.postapi, name="postapi"),
    path("profile/<str:uname>", views.profile, name="profile"),
    path("followapi/<str:name>", views.followapi, name="followapi"),
    path("follow/<str:name>", views.follow, name="follow"),
    path("unfollow/<str:name>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("likesapi/<int:postid>", views.likesapi, name="likesapi")
]
