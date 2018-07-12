from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.views import login as auth_login
from .forms import SignupForm, LoginForm

def signup(request):
    # 인트라넷 이메일 인증 필요
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)  # default: ' /accounts/login/'
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })


def login(request):
    return auth_login(request,
                authentication_form=LoginForm,
                template_name='accounts/login_form.html')

def logout(request):
    pass