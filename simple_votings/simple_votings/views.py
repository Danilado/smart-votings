import datetime
import json
from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from user_profile.forms import AddVoteForm
from user_profile.forms import DescForm
from user_profile.models import UserVote
from user_profile.models import Vote
from user_profile.views import is_moderator


def super_voleyball(request: HttpRequest):  
    return render(request, 'index/index.html')


def vote_list(request: HttpRequest):
    return HttpResponse(
        json.dumps([(vote.theme, vote.description, vote.answers.split(";")) for vote in Vote.objects.all()])
    )


def user_friendly_vote_list(request: HttpRequest):
    return render(request, 'votes/list.html')
    

@permission_required("user_profile.add_uservote")
def description_vote(request: HttpRequest):  # votings description
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

    return render(request, "votes/description_vote.html", context)


@permission_required("user_profile.view_vote")
def show_all(request: HttpRequest):  # all votings
    votes = Vote.objects.all()
    context = {'votes': votes,
               "is_moderator": is_moderator(request.user)}
    return render(request, "votes/all.html", context)


@permission_required("user_profile.add_vote")
def add_new_vote(request: HttpRequest):  # new voting
    context = {}
    form = AddVoteForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        theme = form.cleaned_data["theme"]
        description = form.cleaned_data["description"]
        answers = form.cleaned_data["answers"]
        record = Vote(theme=theme, description=description, answers=answers)
        record.save()
    context['form'] = form
    return render(request, "votes/add.html", context)


@login_required
def profile_statistic(request: HttpRequest):
    if TYPE_CHECKING:
        assert isinstance(request.user, AbstractUser)
    context = {}
    current_user = request.user
    context['user'] = current_user
    time_online = datetime.datetime.now().replace(tzinfo=None) - current_user.last_login.replace(tzinfo=None)
    context['time_online_hour'] = time_online
    context['date_reg'] = current_user.date_joined
    data = UserVote.objects.filter(user=current_user)
    count_of_votes = len(data)
    context['count_of_votes'] = count_of_votes
    context['data'] = data

    return render(request, "accounts/profile_statistic.html", context)


@login_required
def vote_result(request: HttpRequest):
    context = {}
    user_votes = UserVote.objects.filter(vote=99)
    print(user_votes)
    context['vote'] = user_votes[0].vote
    answers = {answer: 0 for answer in user_votes[0].vote.answers.split(";")}

    users_count = 0

    for item in user_votes:
        results = item.results.split(";")
        for result in results:
            users_count += 1
            answers.update({result: answers.get(result, 0) + 1})

    for k, result in answers.items():
        answers.update({k: answers.get(k) / users_count * 100})

    context['answers'] = answers
    return render(request, "votes/result.html", context)
