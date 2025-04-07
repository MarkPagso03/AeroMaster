"""
URL configuration for AeroMaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('base/', views.base_view, name='base'),
    # path('', views.base_view, name='base'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('signup_acc/', views.signup_acc, name='signup_acc'),
    path('', views.landing_view, name="landing"),
    path('home/', views.home_view, name="home"),
    path('mock_exam/', views.exam_view, name="mock_exam"),
    path('login_acc/', views.login_acc, name='login_acc'),
    path('logout/', views.logout_view, name='logout'),
    path('unavailable_page/', views.unavailable_view, name='unavailable'),
    path('back/', views.back_view, name='back'),
    path('administrator/', include('AeroMaster_admin.urls')),
]
