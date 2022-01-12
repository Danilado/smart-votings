from gettext import gettext

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.forms import EmailInput, TextInput, PasswordInput
from django.http import QueryDict


class DescForm(forms.Form):
    CHOICES = [
        ('1', 'YES'), ('2', 'NO')
    ]  # тот кто теперь должен делать подсчет, в бд хранится номер варианта ответа yes - 1, no - 2
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)



class AddVoteForm(forms.Form):
    theme = forms.CharField(label="Название")
    description = forms.CharField(label="Описание")
    answers = forms.CharField(label="Введите варианты ответов, разделяя их знаком ; ")



class RegistrationForm(forms.Form):
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
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        if username not in self.exclude_users and get_user_model().objects.filter(username=username).first():
            self.add_error(
                "username",
                self.error_messages['already_exists']
            )
        return result and username is not None and username and password is not None and email is not None and \
            password and email

    def __init__(self, data: QueryDict, exclude_users=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        if exclude_users is None:
            exclude_users = []
        self.data = data
        self.exclude_users = exclude_users
