from gettext import gettext

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.forms import EmailInput, TextInput, PasswordInput
from django.http import QueryDict
import simple_votings.choice as choice

class DescForm(forms.Form):
    CHOICES = choice.choises
    # Vlastelin a.k.a kotuk: тот кто теперь должен делать подсчет, в бд хранится номер варианта ответа yes - 1, no - 2
    # gospodin: но почему не 0 и 1 ?
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)



class AddVoteForm(forms.Form):  # add new vote
    theme = forms.CharField(label="Название")
    description = forms.CharField(label="Описание")
    answers = forms.CharField(label="Введите варианты ответов, разделяя их знаком ; ")


class RegistrationForm(forms.Form):  # register
    username = UsernameField(widget=TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=gettext("Password"),
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    email = forms.CharField(
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
        if result:
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            email = self.cleaned_data.get('email')
            if username not in self.exclude_users and get_user_model().objects.filter(username=username).first():
                self.add_error(
                    "username",
                    self.error_messages['already_exists']
                )
                result = False
            result = \
                result and username is not None and username and password is not None and email is not None and \
                password and email
        return result

    def __init__(self, *args, **kwargs):
        self.exclude_users = kwargs.get("exclude_users", [])
        if "exclude_users" in kwargs:
            del kwargs["exclude_users"]
        super().__init__(*args, **kwargs)


class CreateReportForm(forms.Form):
    theme = forms.CharField()
    content = forms.CharField()
