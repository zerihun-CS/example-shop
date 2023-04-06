from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            
            return redirect('home_url')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def auditor_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_auditor:            
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func

def auditee_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_auditee:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func


def manager_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_manager:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func


def admin_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_admin:            
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func