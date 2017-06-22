__author__ = 'riros <ivanvalenkov@gmail.com> 23.11.16'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
]
