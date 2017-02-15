__author__ = 'riros <ivanvalenkov@gmail.com> 23.11.16'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^$/(?P<acc_id>[0-9]+)/$', views.user_account_page),

    url(r'loadusers', views.load_users)
]
