from typing import Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser, User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from user_profile.forms import DescForm, RegistrationForm
from user_profile.models import Vote


@login_required
def get_user_profile_page(request: HttpRequest):
    # noinspection PyTypeHints
    request.user: AbstractUser
    assert request.user.is_authenticated

    print(request.user)

    return render(request, "accounts/profile.html")


@login_required
def change_user(request: HttpRequest):
    # noinspection PyTypeHints
    request.user: AbstractUser
    assert request.user.is_authenticated

    context = dict(
        form=RegistrationForm(request.POST, [request.user.username])
    )
    if len(request.POST) > 3 and context['form'].is_valid() and not context['form'].errors:
        print(request.POST)
        request.user.username = context['form'].cleaned_data.get("username", request.user.username)
        request.user.set_password(context['form'].cleaned_data.get("password", request.user.password))
        request.user.email = context['form'].cleaned_data.get("email", request.user.email)
        request.user.save()
        return HttpResponseRedirect("/auth/login")
    return render(request, "registration/change_user.html", context)


def register_user(request: HttpRequest):
    context = dict(
        form=RegistrationForm(request.POST)
    )
    if len(request.POST) > 3:
        if context['form'].is_valid() and not context['form'].errors:
            new_user: Optional[AbstractUser] = User.objects.create_user(
                context['form'].cleaned_data.get('username'),
                context['form'].cleaned_data.get('email'),
                context['form'].cleaned_data.get('password'))
            new_user.save()
            return HttpResponseRedirect('/auth/login')
    register_page_render = render(request, "registration/register.html", context=context)
    return register_page_render


def description_vote(request):
    context = {}
    theme = "None"
    description = "None"
    answer1 = "YES"
    answer2 = "NO"
    user_id = 2
    if request.method == "POST":
        form = DescForm(request.POST)
        result = form.data["choice_field"]
        record = Vote(theme=theme, description=description, answer1=answer1, answer2=answer2, result=result)
        record.save()
        context['form'] = form
    else:
        form = DescForm()

    all_data = Vote.objects.all()

    context['data'] = all_data
    context['id'] = user_id
    context['form'] = form

    return render(request, "description_vote.html", context)


def show_all(request):
    all_data = Vote.objects.all()
    context = {'data': all_data}
    return render(request, "all.html", context)
