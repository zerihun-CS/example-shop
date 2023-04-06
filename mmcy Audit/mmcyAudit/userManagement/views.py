from django.shortcuts import render,redirect
from .forms import AccountAuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
# Create your views here.
@unauthenticated_user
def login_view(request):
    context = {}
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.is_auditor:
                   
                  return redirect('home_url')
                elif user.is_manager:
                    return redirect('home_url')
                elif user.is_auditee:
                    return redirect('home_url')
                elif user.is_superuser:
                    return redirect('/admin/')                
                else:
                    return redirect("login")
        else:
            context['login_form'] = form
            print(form.errors)
            return render(request, "sign-in.html", context)
            

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "sign-in.html", context)



@login_required(login_url='/login/')
def logout_view(request):
	logout(request)
	return redirect('login_url')