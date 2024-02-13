from django.urls import path


from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("user_profile/", views.user_profile, name="user_profile")
]