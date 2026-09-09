from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("feed/", views.feed, name="feed"),
    path("explore/", views.explore, name="explore"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("password/change/", auth_views.PasswordChangeView.as_view(template_name="core/password_change.html", success_url=reverse_lazy("edit_profile")), name="password_change"),
    path("u/<str:username>/", views.profile_view, name="profile"),
    path("u/<str:username>/follow/", views.follow_toggle, name="follow_toggle"),
    path("u/<str:username>/<str:kind>/", views.connections, name="connections"),
    path("posts/<int:post_id>/like/", views.like_toggle, name="like_toggle"),
    path("posts/<int:post_id>/comment/", views.comment_add, name="comment_add"),
    path("posts/<int:post_id>/delete/", views.post_delete, name="post_delete"),
]
