from django.http import JsonResponse
from django.shortcuts import render
from .models import faculty
from AeroMaster.models import Question  # Import the model from AeroMaster

# Create your views here.

def admin_view(request):
    return render(request, 'admin.html')

def faculty_list(request):
    faculties = list(faculty.objects.values('first_name', 'last_name', 'emp_id', 'email'))
    return JsonResponse({'faculties': faculties})