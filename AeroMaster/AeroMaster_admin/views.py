from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import (faculty, ArchiveFaculty, ArchiveStudent, ArchiveQuestion, GeneratedQuestions, ExamSetting,
                     ExamResult, UserFeedback)
from .forms import FacultyForm, StudentForm, AeroMasterAdminForm, QuestionForm
from AeroMaster.models import Student, Question
from AeroMaster.resources import UserResource, QuestionResource, FacultyResource
import random
import json
from collections import Counter
from itertools import zip_longest
from datetime import datetime
from tablib import Dataset


# from AeroMaster.decorators import role_required


# Create your views here.
def login_admin_view(request):
    return render(request, 'login_admin.html')


def login_acc(request):
    if request.method == 'POST':
        logout(request)
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
        if not request.user.is_authenticated or request.user.role not in ['aeromaster_admin']:
            return render(request, 'login_admin.html')
        return view_func(request, *args, **kwargs)

    return wrapper


def faculty_required(view_func):
    """ Custom decorator to restrict access to AeroMaster Admins and Faculty only. """

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ['faculty']:
            return render(request, 'login_admin.html')
        return view_func(request, *args, **kwargs)

    return wrapper


def adminfaculty_required(view_func):
    """ Custom decorator to restrict access to AeroMaster Admins and Faculty only. """

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ['aeromaster_admin', 'faculty']:
            return render(request, 'login_admin.html')
        return view_func(request, *args, **kwargs)

    return wrapper


@adminfaculty_required
def admin_view(request):
    return render(request, 'admin.html')


@admin_required
def add_faculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    else:
        form = FacultyForm()
    return render(request, 'add_faculty.html', {'form': form})


@admin_required
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


@admin_required
def faculty_list(request):
    faculties = faculty.objects.values('first_name', 'last_name', 'emp_id', 'email')
    return render(request, 'view_faculty.html', {'faculties': faculties})


@admin_required
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


@adminfaculty_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


@adminfaculty_required
def edit_student(request, student_id):
    student_member = get_object_or_404(Student, id_number=student_id)
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


@adminfaculty_required
def student_list(request):
    students = Student.objects.values('first_name', 'last_name', 'id_number', 'email')
    return render(request, 'view_student.html', {'students': students})


@adminfaculty_required
def archive_student(request, student_id):
    student_member = get_object_or_404(Student, pk=student_id)
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


@adminfaculty_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form})


@faculty_required
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


@faculty_required
def question_list(request):
    questions = Question.objects.values('id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer',
                                        'subject')
    return render(request, 'view_question.html', {'questions': questions})


@faculty_required
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


@faculty_required
def panel_view(request):
    questions = list(GeneratedQuestions.objects.values(
        'id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'subject'
    ))

    if request.method == "POST":
        # For each form in the POST data, check if valid and save
        for key, value in request.POST.items():
            if key.startswith('subject_'):
                exam_id = key.split('_')[1]
                exam_setting = ExamSetting.objects.get(id=exam_id)
                exam_setting.subject = value
                exam_setting.date_time = request.POST.get(f"date_time_{exam_id}")
                exam_setting.shuffle = request.POST.get(f"shuffle_{exam_id}") == 'on'
                exam_setting.passing_score = request.POST.get(f"passing_score_{exam_id}")
                exam_setting.duration = request.POST.get(f"duration_{exam_id}")
                exam_setting.save()

        return redirect('panel')  # Redirect after saving

    exam_settings = ExamSetting.objects.all()

    questions_json = json.dumps(questions, cls=DjangoJSONEncoder)
    context = {
        'questions_json': questions_json,
        'exam_settings': exam_settings
    }

    return render(request, 'panel.html', context)


@faculty_required
def generate_questions(request):
    GeneratedQuestions.objects.all().delete()

    subjects = ['AERO', 'MATH', 'STRUC', 'ACRM', 'PWRP', 'EEMLE']
    selected_questions = {}

    for subject in subjects:

        # Get all questions for the subject
        questions = list(Question.objects.filter(subject=subject))
        # Randomly pick 50, or fewer if not enough
        selected = random.sample(questions, min(len(questions), 50))
        selected_questions[subject] = []

        for q in selected:
            # Save each selected question to GeneratedQuestions
            GeneratedQuestions.objects.create(
                text=q.text,
                option_a=q.option_a,
                option_b=q.option_b,
                option_c=q.option_c,
                option_d=q.option_d,
                correct_answer=q.correct_answer,
                subject=q.subject,  # optional, if you have a field for this
            )
            selected_questions[subject].append(q.text)

    questions_list = list(
        GeneratedQuestions.objects.all().values('text', 'option_a', 'option_b', 'option_c', 'option_d',
                                                'correct_answer', 'subject'))
    return JsonResponse({'questions': questions_list})


@faculty_required
def dashboard_view(request):
    exam_settings = ExamSetting.objects.all()
    passing_scores = {setting.subject.upper(): setting.passing_score for setting in exam_settings}

    participants = ExamResult.objects.count()
    total_passed = ExamResult.objects.filter(total_result='Passed').count()
    pass_percentage = (total_passed / participants) * 100 if participants > 0 else 0

    passed_per_subject = {
        'AERO': ExamResult.objects.filter(aero_result__gte=passing_scores.get('AERO', 38)).count(),
        'MATH': ExamResult.objects.filter(math_result__gte=passing_scores.get('MATH', 38)).count(),
        'STRUC': ExamResult.objects.filter(struc_result__gte=passing_scores.get('STRUC', 38)).count(),
        'ACRM': ExamResult.objects.filter(acrm_result__gte=passing_scores.get('ACRM', 38)).count(),
        'PWRP': ExamResult.objects.filter(pwrp_result__gte=passing_scores.get('PWRP', 38)).count(),
        'EEMLE': ExamResult.objects.filter(eemle_result__gte=passing_scores.get('EEMLE', 38)).count(),
    }

    failed_per_subject = {
        subject: participants - passed_per_subject[subject]
        for subject in passed_per_subject
    }

    comment_fields = {
        'AERO': UserFeedback.objects.exclude(aero_comments__isnull=True).exclude(aero_comments__exact='').values_list(
            'aero_comments', flat=True),
        'MATH': UserFeedback.objects.exclude(math_comments__isnull=True).exclude(math_comments__exact='').values_list(
            'math_comments', flat=True),
        'STRUC': UserFeedback.objects.exclude(struc_comments__isnull=True).exclude(
            struc_comments__exact='').values_list('struc_comments', flat=True),
        'ACRM': UserFeedback.objects.exclude(acrm_comments__isnull=True).exclude(acrm_comments__exact='').values_list(
            'acrm_comments', flat=True),
        'PWRP': UserFeedback.objects.exclude(pwrp_comments__isnull=True).exclude(pwrp_comments__exact='').values_list(
            'pwrp_comments', flat=True),
        'EEMLE': UserFeedback.objects.exclude(eemle_comments__isnull=True).exclude(
            eemle_comments__exact='').values_list('eemle_comments', flat=True),
    }

    # Combine by rows using zip_longest
    comment_rows = list(zip_longest(
        comment_fields['AERO'],
        comment_fields['MATH'],
        comment_fields['STRUC'],
        comment_fields['ACRM'],
        comment_fields['PWRP'],
        comment_fields['EEMLE'],
        fillvalue=""
    ))

    # Satisfaction stats per subject
    def get_satisfaction_data(subject_prefix):
        feedbacks = UserFeedback.objects.all()
        sat_field = f'{subject_prefix.lower()}_satisfaction'

        satisfaction_counter = Counter(
            getattr(fb, sat_field) for fb in feedbacks if getattr(fb, sat_field) is not None
        )
        return {
            'counts': {
                1: satisfaction_counter.get(1, 0),
                2: satisfaction_counter.get(2, 0),
                3: satisfaction_counter.get(3, 0),
            }
        }

    satisfaction_data = {
        'AERO': get_satisfaction_data('AERO'),
        'MATH': get_satisfaction_data('MATH'),
        'STRUC': get_satisfaction_data('STRUC'),
        'ACRM': get_satisfaction_data('ACRM'),
        'PWRP': get_satisfaction_data('PWRP'),
        'EEMLE': get_satisfaction_data('EEMLE'),
    }

    context = {
        'participants': participants,
        'pass_percentage': round(pass_percentage, 2),
        'passed_per_subject': passed_per_subject,
        'failed_per_subject': failed_per_subject,
        'satisfaction_data': satisfaction_data,
        'comment_headers': list(comment_fields.keys()),
        'comment_rows': comment_rows
    }

    return render(request, 'dashboard.html', context)


def export_user(request):
    resource = UserResource()
    dataset = resource.export()

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"user_{timestamp}.csv"

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def import_user(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            dataset = Dataset()
            new_data = request.FILES['csv_file'].read().decode('utf-8')
            imported_data = dataset.load(new_data, format='csv')

            resource = UserResource()
            result = resource.import_data(imported_data, dry_run=True)  # preview

            if result.has_errors():
                messages.error(request, 'Import failed due to errors in the CSV file.')
                for row in result.invalid_rows:
                    messages.error(request, f"Row error: {row.error}")
            else:
                resource.import_data(imported_data, dry_run=False)  # actually save
                messages.success(request, 'Students imported successfully!')

        except Exception as e:
            messages.error(request, f"An error occurred while importing: {e}")

    return render(request, 'import_user.html')


def export_question(request):
    resource = QuestionResource()
    dataset = resource.export()

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"question_{timestamp}.csv"

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def import_question(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            dataset = Dataset()
            new_data = request.FILES['csv_file'].read().decode('utf-8')
            imported_data = dataset.load(new_data, format='csv')

            resource = QuestionResource()
            result = resource.import_data(imported_data, dry_run=True)  # preview

            if result.has_errors():
                messages.error(request, 'Import failed due to errors in the CSV file.')
                for row in result.invalid_rows:
                    messages.error(request, f"Row error: {row.error}")
            else:
                resource.import_data(imported_data, dry_run=False)  # actually save
                messages.success(request, 'Questions imported successfully!')

        except Exception as e:
            messages.error(request, f"An error occurred while importing: {e}")

    return render(request, 'import_question.html')


def export_faculty(request):
    resource = FacultyResource()
    dataset = resource.export()

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"faculty_{timestamp}.csv"

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def import_faculty(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            dataset = Dataset()
            new_data = request.FILES['csv_file'].read().decode('utf-8')
            imported_data = dataset.load(new_data, format='csv')

            resource = FacultyResource()
            result = resource.import_data(imported_data, dry_run=True)  # preview

            if result.has_errors():
                messages.error(request, 'Import failed due to errors in the CSV file.')
                for row in result.invalid_rows:
                    messages.error(request, f"Row error: {row.error}")
            else:
                resource.import_data(imported_data, dry_run=False)  # actually save
                messages.success(request, 'Faculties imported successfully!')

        except Exception as e:
            messages.error(request, f"An error occurred while importing: {e}")

    return render(request, 'import_faculty.html')
