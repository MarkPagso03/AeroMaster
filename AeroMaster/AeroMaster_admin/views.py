from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import faculty, ArchiveFaculty, ArchiveStudent
from .forms import FacultyForm, StudentForm
from AeroMaster.models import User


# Create your views here.

def admin_view(request):
    return render(request, 'admin.html')


def add_faculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    else:
        form = FacultyForm()
    return render(request, 'add_faculty.html', {'form': form})


def edit_faculty(request, faculty_id):
    faculty_member = get_object_or_404(faculty, pk=faculty_id)
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty_member)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = FacultyForm(instance=faculty_member)
    return render(request, 'edit_faculty.html',
                  {'form': form, 'faculty_id': faculty_id, 'faculty_member': faculty_member})


def faculty_list(request):
    faculties = faculty.objects.values('first_name', 'last_name', 'emp_id', 'email')
    return render(request, 'view_faculty.html', {'faculties': faculties})


def archive_faculty(request, faculty_id):
    faculty_member = get_object_or_404(faculty, emp_id=faculty_id)
    ArchiveFaculty.objects.create(
        first_name=faculty_member.first_name,
        last_name=faculty_member.last_name,
        emp_id=faculty_member.emp_id,
        email=faculty_member.email
    )
    faculty_member.delete()
    return redirect('faculty_list')


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


def edit_student(request, student_id):
    student_member = get_object_or_404(User, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student_member)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = StudentForm(instance=student_member)
    return render(request, 'edit_student.html',
                  {'form': form, 'student_id': student_id, 'student_member': student_member})


def student_list(request):
    students = User.objects.values('first_name', 'last_name', 'id_number', 'email')
    return render(request, 'view_student.html', {'students': students})


def archive_student(request, student_id):
    student_member = get_object_or_404(User, pk=student_id)
    ArchiveStudent.objects.create(
        first_name=student_member.first_name,
        last_name=student_member.last_name,
        id_number=student_member.id_number,
        email=student_member.email
    )
    student_member.delete()
    return redirect('student_list')
