from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "game"

urlpatterns = [
    path("", views.user_login_view, name="login"),
    path("login/", views.user_login_view, name="login"),
    path("game/", views.game_view, name="game"),
    path("highscore/", views.highscore_view, name="highscore"),
    path("logout/", LogoutView.as_view(next_page="game:login"), name="logout"),
]