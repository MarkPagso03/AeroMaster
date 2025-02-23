from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from .forms import LoginForm
from django.db import models
from django.contrib.auth import authenticate, login

def base_view(request):
    return render(request, 'base.html')

def dashboard_view(request):
    return render(request, 'admin_base.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def landing_view(request):
    return render(request, 'landing_page.html')

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
            login(request, user)  # Auto login
            print("saved!")
            return redirect('home')  # Redirect to homepage
        print("not saved!2")

    else:
        print("not saved!")
        form = SignUpForm()

    print("sign_up!")
    return render(request, 'signup.html', {'form': form})

def login_acc(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            id_number = form.cleaned_data.get('id_number')
            password = form.cleaned_data.get('password')
            user = authenticate(id_number = id_number, password = password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request,'login.html',{form: form, 'msg': msg})