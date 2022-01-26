from typing import Optional, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin, AnonymousUser
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from user_profile.forms import RegistrationForm, AddVoteForm, CreateReportForm
from user_profile.models import Vote, Report


def is_moderator(user: Union[PermissionsMixin, AnonymousUser]) -> bool:
    return user.groups.filter(name="Moderator").first() is not None


def post_or_none(request: HttpRequest):
    return request.POST if request.method == "POST" else None


@permission_required("auth.view_user")
@login_required
def get_user_profile_page(request: HttpRequest):
    context = {
        'name': request.user.username,
        'date_joined': str(request.user.date_joined),
        'last_login': str(request.user.last_login),
        "is_moderator": is_moderator(request.user)
    }
    print(request.user)
    return render(request, "accounts/profile.html", context)


@permission_required("auth.change_user")
@login_required
def change_user(request: HttpRequest):  # change current user
    context = dict(
        form=RegistrationForm(
            post_or_none(request), exclude_users=[request.user.username], initial={
                "username": request.user.username,
                "email": request.user.email
            }
        )
    )
    print("\n".join(f"{field[0]}, {field[1].initial}" for field in context['form'].fields.items()))
    if len(request.POST) > 3 and context['form'].is_valid() and not context['form'].errors:
        print(request.POST)
        request.user.username = context['form'].cleaned_data.get("username", request.user.username)
        request.user.set_password(context['form'].cleaned_data.get("password", request.user.password))
        request.user.email = context['form'].cleaned_data.get("email", request.user.email)
        request.user.save()
        return HttpResponseRedirect(reverse("login"))
    return render(request, "registration/change_user.html", context)


def register_user(request: HttpRequest):  # register new user
    context = dict(
        form=RegistrationForm(request.POST)
    )
    if len(request.POST) > 3:
        if context['form'].is_valid() and not context['form'].errors:
            new_user: Optional[AbstractUser] = get_user_model().objects.create_user(
                context['form'].cleaned_data.get('username'),
                context['form'].cleaned_data.get('email'),
                context['form'].cleaned_data.get('password'))
            new_user.groups.add(Group.objects.filter(name="Normal user").first())
            new_user.save()
            return HttpResponseRedirect(reverse("login"))
    register_page_render = render(request, "registration/register.html", context=context)
    return register_page_render


@permission_required("user_profile.change_vote")
@login_required
def change_vote(request: HttpRequest):
    context = dict(
        form=AddVoteForm(post_or_none(request)),
        old_theme=request.POST.get("old_theme") if request.method == "POST" else request.GET.get("old_theme")
    )
    if context['form'].is_valid() and not context['form'].errors:
        vote: Optional[Vote] = Vote.objects.filter(theme=context['old_theme']).first()
        valid_old_theme = context['old_theme'] is not None and vote
        if valid_old_theme:
            vote.theme = context['form'].cleaned_data.get("theme")
            vote.description = context['form'].cleaned_data.get('description')
            vote.answers = context['form'].cleaned_data.get('answers')
            vote.save()
            return HttpResponseRedirect(reverse("list_votings"))
    return render(request, "votes/edit.html", context)


@permission_required("user_profile.add_report")
@login_required
def create_report(request: HttpRequest):
    context = dict(
        form=CreateReportForm(post_or_none(request)),
        id=request.GET.get("id") if request.method == "GET" else request.POST.get("id")
    )
    context['vote'] = Vote.objects.filter(id=context['id']).first()
    if context['id'] is None or context['vote'] is None:
        return HttpResponseBadRequest()
    if context['form'].is_valid():
        report = Report(author=request.user,
                        theme=context['form'].cleaned_data['theme'],
                        content=context['form'].cleaned_data['content'],
                        vote=context['vote'])
        report.save()
        return HttpResponseRedirect(reverse("list_votings"))
    return render(request, "votes/report/create.html", context)


@permission_required("user_profile.view_report")
@login_required
def reports_list(request: HttpRequest):
    context = {"reports": Report.objects.all()}
    return render(request, "votes/report/list.html", context)


@permission_required("user_profile.delete_vote")
@login_required
def delete_vote(request: HttpRequest):
    vote: Optional[Vote] = Vote.objects.filter(id=int(request.POST.get('id', ""))).first()  # Почему +1? Не знаю.
    valid_request = request.method == "POST" and "id" in request.POST and vote is not None
    if not valid_request:
        return HttpResponseBadRequest()
    vote.delete()
    return HttpResponseRedirect(reverse("list_votings"))


@permission_required("user_profile.delete_report")
@login_required
def delete_report(request: HttpRequest):
    report: Optional[Report] = Report.objects.filter(id=int(request.POST.get('id', ""))).first()
    valid_request = request.method == "POST" and "id" in request.POST and report is not None
    if not valid_request:
        return HttpResponseBadRequest()
    report.delete()
    return HttpResponseRedirect(reverse("report_list"))
