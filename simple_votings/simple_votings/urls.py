from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from simple_votings.views import *
from user_profile.views import *

urlpatterns = [
    path("", super_voleyball, name="index"),  # super_volleyball
    path("accounts/profile", get_user_profile_page, name="profile"),  # profile page
    path("accounts/profile/statistic", profile_statistic, name="profile_statistic"),
    path("admin/", admin.site.urls),
    path("api/get_vote_list", vote_list, name="vote_list_api"),
    path("auth/", include('user_profile.urls')),  # login page
    path("accounts/profile", get_user_profile_page),  # profile page
    path("get_vote_list/", vote_list),
    path("vote/submit", vote_n_goback),
    path("accounts/profile/statistic", profile_statistic),
    path("vote/add", add_new_vote, name="add_vote"),  # new vote page
    path("vote/delete", delete_vote, name="delete_vote"),
    path("vote/description", description_vote, name="description"),
    path("vote/edit", change_vote, name="change_vote"),
    path("vote/list", user_friendly_vote_list, name="vote_list"),
    path("vote/report/create", create_report, name="create_report"),
    path("vote/report/delete", delete_report, name="delete_report"),
    path("vote/report/table", reports_list, name="report_list"),
    path("vote/show", show_all, name="list_votings"),  # all votings
    path("vote_result", vote_result, name="vote_result"),
]

urlpatterns += staticfiles_urlpatterns()
