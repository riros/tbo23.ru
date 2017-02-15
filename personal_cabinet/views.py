from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_page

from django.http.response import HttpResponse
from .models import *


# @cache_page(60 * 15)
@login_required()
def user_account_page(request, acc_id):
    return render(request, 'personal_cabinet/index.html', context={'acc_id': acc_id})


@login_required()
def index(request):
    return render(request, 'personal_cabinet/index.html', context={
        'accounts': Account.objects.all().filter(euser=request.user)
    })


# @login_required()
def load_users(req):
    if req.user.is_authenticated:
        return render(req, 'personal_cabinet/ok.html')
    else:
        return render(req, 'personal_cabinet/error.html')
