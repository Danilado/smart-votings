import datetime

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

def description_vote(request: HttpRequest): # votings description
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


def show_all(request: HttpRequest): # all votings
    all_data = Vote.objects.all()
    context = {'data': all_data}
    return render(request, "all.html", context)


def add_new_vote(request: HttpRequest): # new voting
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


@login_required
def profile_statistic(request: HttpRequest):
    context = {}
    current_user = request.user
    #---------------------------добавление в бд
    #new_vote = Vote(id=99, theme="Hello", description='BdsgaB', answers="a;b;c;f")
    #new_vote.save()
    #record = UserVote(vote=new_vote, results='c;b', user = current_user)
    #record.save()
    #---------------------------
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
    data = UserVote.objects.filter(vote=99)
    print(data)
    context['vote'] = data[0].vote
    ans = {}

    for item in data[0].vote.answers:
        ans.update({item: 0})

    users_count = 0

    for item in data:
        results = item.results.split(";")
        for el in results:
            users_count += 1
            if ans.get(el) is None:
                ans.update({el: 1})
            else:
                ans.update({el: ans.get(el) + 1})

    for k, el in ans.items():
        ans.update({k: ans.get(k) / users_count * 100})

    context['ans'] = ans
    return render(request, "vote_result.html", context)
