from django.shortcuts import render

def base_view(request):
    return render(request, 'base.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def landing_view(request):
    return render(request, 'landing_page.html')

def home_view(request):
    return render(request, 'home.html')