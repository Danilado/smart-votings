from typing import Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import AbstractUser, User
from django.forms import CharField, EmailInput, TextInput, PasswordInput, forms
from django.http import HttpRequest, HttpResponseRedirect, QueryDict
from django.shortcuts import render
from django.utils.translation import gettext

from user_profile.forms import AddVoteForm
from user_profile.forms import DescForm
from user_profile.models import UserVote
from user_profile.models import Vote


@login_required
def get_user_profile_page(request: HttpRequest):
    # noinspection PyTypeHints
    request.user: AbstractUser
    assert request.user.is_authenticated

    print(request.user)

    return render(request, "accounts/profile.html")


class RegistrationForm(forms.Form):
    username = UsernameField(widget=TextInput(attrs={'autofocus': True}))
    password = CharField(
        label=gettext("Password"),
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    email = CharField(
        label=gettext("Email"),
        widget=EmailInput(),
    )
    error_messages = {
        'already_exists': gettext(
            "The user with that login already exists."
        ),
    }

    def is_valid(self):
        result = super().is_valid()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).first():
            self.add_error(
                "username",
                self.error_messages['already_exists']
            )
        return result and username is not None and username and password is not None and email is not None and \
            password and email

    def __init__(self, data: QueryDict, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.data = data


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


def description_vote(request: HttpRequest):
    context = {}
    description = "None"
    answer1 = "YES"
    answer2 = "NO"
    user_id = 2
    form = DescForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        result = form.data["choice_field"]
        record = UserVote(description=description, answer1=answer1, answer2=answer2, result=result)
        record.save()
        context['form'] = form

    all_data = UserVote.objects.all()

    context['data'] = all_data
    context['id'] = user_id
    context['form'] = form

    return render(request, "description_vote.html", context)


def show_all(request: HttpRequest):
    all_data = Vote.objects.all()
    context = {'data': all_data}
    return render(request, "all.html", context)


def add_new_vote(request: HttpRequest):
    context = {}
    form = AddVoteForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        theme = form.data["theme"]
        description = form.data["description"]
        answers = form.data["answers"]
        record = Vote(theme=theme, description=description, answers=answers)
        record.save()
    context['form'] = form
    return render(request, "add.html", context)
