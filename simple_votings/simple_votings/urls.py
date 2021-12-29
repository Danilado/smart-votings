"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from simple_votings import settings

from user_profile.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include('user_profile.urls')),
    path("accounts/profile", get_user_profile_page),
    path("description/", description_vote),
    path("show/", show_all),
    path("add/", add_new_vote)
]

urlpatterns += staticfiles_urlpatterns()
