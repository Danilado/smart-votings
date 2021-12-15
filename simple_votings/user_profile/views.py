from typing import Union

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser, User, AbstractUser
from django.http import HttpRequest, Http404
from django.shortcuts import render


@login_required
def get_user_profile(request: HttpRequest):
    # noinspection PyTypeHints
    request.user: Union[User, AbstractUser]
    assert request.user.is_authenticated

    print(request.user)

    return render(request, "accounts/profile.html")


def register_page(request: HttpRequest):
    pass
