from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("button_click_tracking_main_page")
            else:
                form = UserProfileForm
                return render(request, 'login.html', {'form': form, 'invalid': True})
        else:
            return render(request, 'login.html', {'form': form, 'invalid': True})
    else:
        if request.user.is_authenticated:
            return redirect("button_click_tracking_main_page")
        else:
            form = UserProfileForm
            return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/login')
