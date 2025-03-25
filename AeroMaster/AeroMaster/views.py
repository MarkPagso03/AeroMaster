from django.shortcuts import render, redirect
from django.contrib.auth import login

from . import settings
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout


def base_view(request):
    return render(request, 'base.html')


def unavailable_view(request):
    return render(request, 'curr_unavailable.html')


@login_required(login_url='/')
def back_view(request):
    return render(request, 'home.html')


def dashboard_view(request):
    return render(request, 'admin_base.html')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/home')
def login_view(request):
    return render(request, 'login.html')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/home')
def signup_view(request):
    return render(request, 'signup.html')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/home')
def landing_view(request):
    return render(request, 'landing_page.html')


@login_required(login_url='/login')
def home_view(request):
    return render(request, 'home.html')


def mock_view(request):
    return render(request, 'mock_exam_page.html')


def signup_acc(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("valid")
            user = form.save(commit=False)  # Prevent immediate save
            user.save()
            login(request, user, backend='AeroMaster.authentication.UserBackend')  # Auto login
            print("User authenticated?", request.user.is_authenticated)
            print("saved!")
            return redirect('home')  # Redirect to homepage
        print("not saved!2")

    else:
        print("not saved!")
        form = SignUpForm()

    print("sign_up!")
    return render(request, 'signup.html', {'form': form})


def login_acc(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data['id_number']
            password = form.cleaned_data['password']
            keep_logged_in = form.cleaned_data.get('keep_logged_in')

            user = authenticate(request, id_number=id_number, password=password)
            if user is not None:
                login(request, user)

                # Set session expiry based on "Keep me logged in"
                if keep_logged_in:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)  # Default expiry (e.g., 2 hours)
                else:
                    request.session.set_expiry(0)  # Expires when the browser closes

                return redirect('home')
            else:
                return render(request, 'landing_page.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'landing_page.html', {'form': form})


def logout_view(request):
    """ Logs out the user and redirects to the login page """
    logout(request)
    return redirect('/')  # Change to your login/home page
