from django.shortcuts import render

from django.http.response import HttpResponse


# Create your views here.

def user_account_page(request, acc_id):
    return HttpResponse("Acc id %s" % acc_id)
