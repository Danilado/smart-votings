from typing import Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser, User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from user_profile.forms import AddVoteForm
from user_profile.forms import DescForm
from user_profile.models import UserVote
from user_profile.models import Vote

def super_voleyball(request: HttpRequest):
    return render(request, 'whatever/tmp_index.html')

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
