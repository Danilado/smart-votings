from typing import Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import AbstractUser, User
from django.forms import CharField, EmailInput, TextInput, PasswordInput, forms
from django.http import HttpRequest, HttpResponseRedirect, QueryDict
from django.shortcuts import render
from django.utils.translation import gettext

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

def description_vote(request):
    data = Vote.objects.all()
    theme = "None"
    description = "None"
    answer1 = "YES"
    answer2 = "NO"
    id = 1
    f = 0
    s = 0
    if request.method == "POST":
        for item in data:
            if item.id == id:
                f = id.first + 1
                pass
        record = Vote(theme=theme, description=description, answer1="засчитал", answer2=answer2)
        record.save()
    if request.method == "POST":
        for item in data:
            if item.id == id:
                s = id.second + 1
                pass
        record = Vote(theme=theme, description=description, answer1=answer1, answer2="засчитал")
        record.save()
    else:
        record = Vote(theme=theme, description=description, answer1=answer1, answer2=answer2)
        record.save()

    all_data = Vote.objects.all()
    context = {}
    context['data'] = all_data
    context['id'] = id




    return render(request, "description_vote.html", context)
