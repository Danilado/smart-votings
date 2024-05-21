import datetime
import json
from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from user_profile.forms import AddVoteForm
from user_profile.forms import DescForm
from user_profile.models import UserVote
from user_profile.models import Vote
from user_profile.views import is_moderator
import simple_votings.choice as choice
from django.urls import reverse

def super_voleyball(request: HttpRequest):  
    return render(request, 'index/index.html')


def vote_list(request: HttpRequest):
    return HttpResponse(
        json.dumps([(vote.theme, vote.description, vote.answers.split(";")) for vote in Vote.objects.all()])
    )


def user_friendly_vote_list(request: HttpRequest):
    return render(request, 'votes/list.html')
    

@permission_required("user_profile.add_uservote")
def vote_n_goback(request: HttpRequest):     # Gospodin: Я ваш родственник
    id = request.GET.get('id')
    var = request.GET.get('choise')
    count_od_users = 0
    user_id = request.user.id
    #print(f'userid: {user_id} id: {id} choise: {var}')
    for i in UserVote.objects.all():
        if str(i.vote_id) == str(id) and str(i.user_id) == str(user_id):
            count_od_users = 1
    if count_od_users == 0:
        record = UserVote(vote_id=id, results=var, user_id=request.user.id)
        record.save()

    return HttpResponseRedirect(reverse("vote_list"))


@permission_required("user_profile.add_uservote")
def description_vote(request: HttpRequest):  # votings description
    context = {}
    id = int(request.GET.get('id'))
    all_data = Vote.objects.all()
    choice.choises = []
    v = []
    for item in all_data:
        if item.id == id:
            v = item
            count = 0
            for i in item.answers.split(";"):
                choice.choises.append((count, i))
                count += 1
            description = item.description
    print(choice.choises, end="\nend\n")
    form = DescForm(request.POST if request.method == "POST" else None)
    print(form.CHOICES)
    form.CHOICES = choice.choises
    print(form.CHOICES)
    form.CHOICES = [(0, '123'), (1, '321')]
    form = DescForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        print(choice.choises)
        print("qwe")
        result = form.data["choice_field"]
        record = UserVote(results=result)
        record.save()
        context['form'] = form
    context['data'] = all_data
    context['id'] = id
    user_votes = UserVote.objects.all()
    context['user_votes'] = user_votes
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
        return user_friendly_vote_list(request)
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
    count_of_votes = data.count()
    context['count_of_votes'] = count_of_votes
    context['data'] = data
    ans_word = {}
    for item in data:
        ans_word.update({item.vote : item.vote.answers.split(";")[int(item.results) - 1]})
    context['ans_word'] = ans_word
    context['user_votes'] = data

    return render(request, "accounts/profile_statistic.html", context)


@login_required
def vote_result(request: HttpRequest):
    context = {}
    data = UserVote.objects.filter(vote=1)
    context['vote'] = data[0].vote
    answers = {}

    for item in data[0].vote.answers.split(";"):
        answers.update({item: 0})

    users_count = 0

    for item in data:
        results = item.results
        users_count += 1
        if answers.get(results) is None:
            answers.update({item.vote.answers.split(";")[int(results) - 1]: 1})
        else:
            answers.update({item.vote.answers.split(";")[int(results) - 1]: answers.get(results) + 1})

    for k, result in answers.items():
        answers.update({k: answers.get(k) / users_count * 100})
    context['answers'] = answers
    return render(request, "votes/result.html", context)
