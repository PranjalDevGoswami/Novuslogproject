from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# def unauthenitcated_user(views_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('/')
#         else:
#             return views_func(request, *args, **kwargs)


#     return wrapper_func



def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request,"You don't have permission",extra_tags="alert-danger")
                return redirect('/')
        return _wrapped_view
    return decorator
