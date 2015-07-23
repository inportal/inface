# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from inface.uc.views import *
from inface.uc.decorators import *

urlpatterns = [
    url(r'^user/list/$', UsersListView.as_view(), name="user_list_view"),
    ]