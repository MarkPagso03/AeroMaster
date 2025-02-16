from django.shortcuts import render

def base_view(request):
    return render(request, 'base.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')