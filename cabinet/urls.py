__author__ = 'riros <ivanvalenkov@gmail.com> 23.11.16'

from django.conf.urls import url
from . import views
from django.contrib.admin.sites import AdminSite

urlpatterns = [
    url(r'^$', views.index , name='index'),
    url(r'^(?P<acc_id>[0-9]+)/$', views.user_account_page),
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^logout/$', views.logout)

    # url(r'^loadusers', views.load_users)
]
