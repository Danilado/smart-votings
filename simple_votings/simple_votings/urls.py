from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from simple_votings.views import *
from user_profile.views import *

urlpatterns = [
    path("", super_voleyball),  # super_volleyball
    path("admin/", admin.site.urls),
    path("auth/", include('user_profile.urls')),  # login page
    path("accounts/profile", get_user_profile_page),  # profile page
    path("description/", description_vote),
    path("show/", show_all),  # all votings
    path("add/", add_new_vote),  # new vote page
    path("edit/", change_vote),
    path("accounts/profile/statistic", profile_statistic),
    path("vote_result", vote_result),
    path("vote/delete", delete_vote),
    path("vote/report/create", create_report),
    path("vote/report/table", report_table),
    path("vote/report/delete", delete_report)
]

urlpatterns += staticfiles_urlpatterns()
