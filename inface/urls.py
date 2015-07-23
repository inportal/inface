"""inface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib.auth.views import logout
from inface.uc.views import UserLoginView
# from django.contrib import admin

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', logout, {'next_page':'/login/'}, name='home_view'),
    url(r'^login/$', UserLoginView.as_view(), name="login_view"),
    url(r'^logout/$', logout, {'next_page':'/login/'}, name='logout_view'),
    url(r'^uc/', include('inface.uc.urls')),
]



