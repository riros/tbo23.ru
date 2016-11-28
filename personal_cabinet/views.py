from django.shortcuts import render
from django.views.decorators.cache import cache_page

from django.http.response import HttpResponse

#@cache_page(60 * 15)
def user_account_page(request, acc_id):
    return render(request, 'personal_cabinet/test.html', context={'acc_id': acc_id})
