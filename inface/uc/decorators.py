# coding: utf-8
from functools import wraps
from django.http.response import Http404
from inface.uc.models import MyUser

def user_access_required(view_func):
    @wraps(view_func)
    def _check(request, *args, **kwargs):
        if request.user.is_active:
            if request.user.is_admin:
                return view_func(request, *args, **kwargs)
            else:
                raise Http404()
        raise Http404()
    return _check