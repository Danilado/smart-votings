from django.contrib import admin
from django.urls import path

from vote_stats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page)
]
