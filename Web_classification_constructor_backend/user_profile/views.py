from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Проверка данных пользователя (должны быть функция,
            # которая проверит есть ли пользователь в БД и вернет True/False)
            # сейчас заглушка
            check_user_data = True
            if check_user_data:
                # user = UserProfile.objects.get(username=username)
                # login(request, user)
                return redirect('/1')
            else:
                form = UserProfileForm
                return render(request, 'login.html', {'form': form, 'invalid': True})
    else:
        if request.user.is_authenticated:
            return redirect('/1')
        else:
            form = UserProfileForm
            return render(request, 'login.html', {'form': form})


def logout(request):
    # logout(request)
    return redirect('/login')
