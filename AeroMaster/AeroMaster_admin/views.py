from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import faculty, ArchiveFaculty, ArchiveStudent, ArchiveQuestion
from .forms import FacultyForm, StudentForm, AeroMasterAdminForm, QuestionForm
from AeroMaster.models import User, Question


# from AeroMaster.decorators import role_required


# Create your views here.
def login_admin_view(request):
    return render(request, 'login_admin.html')


def login_acc(request):
    if request.method == 'POST':
        form = AeroMasterAdminForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print("authe")
                return redirect('AeroMaster_admin')
            else:
                print("authe1")
                return render(request, 'login_admin.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = AeroMasterAdminForm()
        print("authe3")
    return render(request, 'login_admin.html', {'form': form})


def admin_required(view_func):
    """ Custom decorator to restrict access to AeroMaster Admins and Faculty only. """

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ['aeromaster_admin', 'faculty']:
            return render(request, 'login_admin.html')
        return view_func(request, *args, **kwargs)

    return wrapper



@admin_required
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
    faculty_member = get_object_or_404(faculty, emp_id=faculty_id)
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
    student_member = get_object_or_404(User, id_number=student_id)
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


def logout_view(request):
    """ Logs out the user and redirects to the login page """
    logout(request)
    return redirect('AeroMaster_admin')


def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form})


def edit_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = QuestionForm(instance=question)
    return render(request, 'edit_question.html',
                  {'form': form, 'question_id': id, 'question': question})


def question_list(request):
    questions = Question.objects.values('id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer',
                                        'subject')
    return render(request, 'view_question.html', {'questions': questions})


def archive_question(request, id):
    question = get_object_or_404(Question, id=id)
    ArchiveQuestion.objects.create(
        text=question.text,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_answer=question.correct_answer,
        subject=question.subject
    )
    question.delete()
    return redirect('question_list')
