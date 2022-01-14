from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from simple_votings.views import *
from user_profile.views import *

urlpatterns = [
    path("", super_voleyball),
    path("admin/", admin.site.urls),
    path("auth/", include('user_profile.urls')),
    path("accounts/profile", get_user_profile_page),
    path("description/", description_vote),
    path("show/", show_all),
    path("add/", add_new_vote)
]

urlpatterns += staticfiles_urlpatterns()
