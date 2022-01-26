import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser, User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from user_profile.forms import AddVoteForm
from user_profile.forms import DescForm
from user_profile.models import UserVote
from user_profile.models import Vote
from user_profile.views import is_moderator
import simple_votings.choice as choice



def super_voleyball(request: HttpRequest):
    return render(request, 'whatever/tmp_index.html')


def vote_list(request: HttpRequest):        # Рубрика очумелые ручки
    buffer = []
    for item in Vote.objects.all():         # Вот не нравится мне это всё, но так плевать....
        buffer.append([item.theme, item.description, item.answers.split(";")]) 
    buffer = str(buffer).replace("'", '"')  # Нелегальная херотень
    return HttpResponse(buffer)


def user_friendly_vote_list(request: HttpRequest):
    return render(request, 'list.html')
    

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

    return render(request, 'goback.html')


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
    context['form'] = form

    return render(request, "description_vote.html", context)


@permission_required("user_profile.view_vote")
def show_all(request: HttpRequest):  # all votings
    all_data = Vote.objects.all()
    context = {'data': all_data,
               "is_moderator": is_moderator(request.user)}
    return render(request, "all.html", context)


@permission_required("user_profile.add_vote")
def add_new_vote(request: HttpRequest):  # new voting
    context = {}
    form = AddVoteForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        theme = form.data["theme"]
        description = form.data["description"]
        answers = form.data["answers"]
        record = Vote(theme=theme, description=description, answers=answers, users='')
        record.save()
    context['form'] = form
    return render(request, "add.html", context)


@login_required
def profile_statistic(request: HttpRequest):
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
    data = UserVote.objects.filter(vote=99)
    print(data)
    context['vote'] = data[0].vote
    ans = {}

    for item in data[0].vote.answers.split(";"):
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
