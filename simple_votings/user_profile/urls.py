from django.urls import path, include

from user_profile.views import register_user, change_user

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("change", change_user, name="change_user"),  # change user page
    path("register", register_user, name="register_user")  # register page
]
