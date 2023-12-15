from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps
from django.http import HttpResponseBadRequest


def unauthenitcated_user(views_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('')
        else:
            return views_func(request, *args, **kwargs)


    return wrapper_func
