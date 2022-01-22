from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from simple_votings.views import *
from user_profile.views import *

urlpatterns = [
    path("", super_voleyball, name="index"),  # super_volleyball
    path("admin/", admin.site.urls),
    path("auth/", include('user_profile.urls')),  # login page
    path("accounts/profile", get_user_profile_page, name="profile"),  # profile page
    path("description/", description_vote, name="description"),
    path("show/", show_all, name="list_votings"),  # all votings
    path("add/", add_new_vote, name="add_vote"),  # new vote page
    path("edit/", change_vote, name="change_vote"),
    path("get_vote_list/", vote_list, name="deprecated_vote_list"),
    path("list/", user_friendly_vote_list, name="vote_list"),
    path("accounts/profile/statistic", profile_statistic, name="account_profile"),
    path("vote_result", vote_result, name="vote_result"),
    path("vote/delete", delete_vote, name="delete_vote"),
    path("vote/report/create", create_report, name="create_report"),
    path("vote/report/table", report_table, name="report_list"),
    path("vote/report/delete", delete_report, name="delete_report"),
]

urlpatterns += staticfiles_urlpatterns()
