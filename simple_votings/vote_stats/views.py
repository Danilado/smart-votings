from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from .models import Votings
from django.db.models import Sum

# Create your views here.


def index_page(request):
    sum_vote_yes = Votings.objects.aggregate(Sum('voted_yes'))['voted_yes__sum']
    sum_vote_no = Votings.objects.aggregate(Sum('voted_no'))['voted_no__sum']
    compare = ''
    sum_vote = sum_vote_yes + sum_vote_no
    if sum_vote_yes == sum_vote_no:
        compare = 'столько же, сколько и'
    elif sum_vote_yes > sum_vote_no:
        compare = f'больше на {round((float(sum_vote_yes) / float(sum_vote_no) - 1) * 100)}%, чем'
    else:
        compare = f'меньше на {round((float(sum_vote_no) / float(sum_vote_yes) - 1) * 100)}%, чем'
    context = {
        'sum_voted_yes':sum_vote_yes,
        'sum_voted_no':sum_vote_no,
        'sum_voted': sum_vote,
        'compare':compare
    }

    return render(request, 'index.html', context)
