import random

from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import localtime, now
from django.contrib import messages
from django.contrib.auth import login

from . import settings
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .models import Student
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from AeroMaster_admin.models import ExamSetting, GeneratedQuestions, ExamResult, UserFeedback


def user_required(view_func):
    """ Custom decorator to restrict access to AeroMaster Admins only. """

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'user':
            return render(request, 'landing_page.html')
        return view_func(request, *args, **kwargs)

    return wrapper


def base_view(request):
    return render(request, 'base.html')


def unavailable_view(request):
    return render(request, 'curr_unavailable.html')


@login_required(login_url='/')
def back_view(request):
    return render(request, 'home.html')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/home')
def login_view(request):
    return render(request, 'login.html')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/home')
def signup_view(request):
    return render(request, 'signup.html')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/home')
def landing_view(request):
    return render(request, 'landing_page.html')


@user_required
def home_view(request):
    def get_exam(subject_code):
        try:
            exam = ExamSetting.objects.get(subject=subject_code)
            exam.date_time = localtime(exam.date_time)
            exam.end_time = exam.date_time + timezone.timedelta(minutes=exam.duration)

            return exam
        except ExamSetting.DoesNotExist:
            return None

    context = {
        'aero_setting': get_exam('AERO'),
        'eemle_setting': get_exam('EEMLE'),
        'acrm_setting': get_exam('ACRM'),
        'math_setting': get_exam('MATH'),
        'struc_setting': get_exam('STRUC'),
        'pwrp_setting': get_exam('PWRP'),
    }

    return render(request, 'home.html', context)


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
        logout(request)
        form = LoginForm(request.POST)
        print('logged in1')
        if form.is_valid():
            id_number = form.cleaned_data['id_number']
            password = form.cleaned_data['password']
            keep_logged_in = form.cleaned_data.get('keep_logged_in')
            print('logged in2')
            user = authenticate(request, id_number=id_number, password=password)
            if user is not None:
                print('logged in3')
                login(request, user)

                # Set session expiry based on "Keep me logged in"
                if keep_logged_in:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)  # Default expiry (e.g., 2 hours)
                else:
                    request.session.set_expiry(0)  # Expires when the browser closes
                print('logged in')
                return redirect('home')
            else:
                print('logged in4')
                return render(request, 'landing_page.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        print('logged in5')
        form = LoginForm()
    return render(request, 'landing_page.html', {'form': form})


def logout_view(request):
    """ Logs out the user and redirects to the login page """
    logout(request)
    return redirect('landing')


@login_required
def exam_view(request, subject):
    # Map subject to the result field in the model
    subject_field_map = {
        'AERO': 'aero_result',
        'MATH': 'math_result',
        'STRUC': 'struc_result',
        'ACRM': 'acrm_result',
        'PWRP': 'pwrp_result',
        'EEMLE': 'eemle_result',
    }

    # Get student's result
    student_id = request.user.id_number
    exam_result, _ = ExamResult.objects.get_or_create(student_id=student_id)
    exam_setting = ExamSetting.objects.get(subject=subject)
    passing_score = exam_setting.passing_score
    questions = list(GeneratedQuestions.objects.filter(subject=subject))

    if exam_setting.shuffle is True:
        random.shuffle(questions)

    current_time = now()
    exam_start_time = localtime(exam_setting.date_time)
    exam_end_time = exam_start_time + timezone.timedelta(minutes=exam_setting.duration)

    if not (exam_start_time <= current_time <= exam_end_time):
        messages.success(request, 'Not scheduled right now.')
        return redirect('home')

    if subject in subject_field_map:
        subject_field = subject_field_map[subject]
        existing_score = getattr(exam_result, subject_field, None)

        if existing_score is not None:
            # Questions are needed for rendering the previous results
            questions = GeneratedQuestions.objects.filter(subject=subject)
            total = questions.count()
            percentage = (existing_score / total) * 100 if total > 0 else 0
            passed = existing_score >= passing_score

            '''return render(request, 'exam_results.html', {
                'score': existing_score,
                'total': total,
                'results': None,  # You can store user answers if needed
                'subject': subject,
                'percentage': round(percentage, 2),
                'passed': passed,
            })'''

            return redirect('exam_result', subject=subject)

    return render(request, 'exam.html', {'subject': subject, 'questions': questions, 'exam_end_time': exam_end_time})


@login_required
def exam_result(request, subject):
    student_id = request.user.id_number
    questions = GeneratedQuestions.objects.filter(subject=subject)
    exam_setting = ExamSetting.objects.get(subject=subject)
    passing_score = exam_setting.passing_score
    exam_result, _ = ExamResult.objects.get_or_create(student_id=student_id)

    subject_field_map_result = {
        'AERO': 'aero_result',
        'MATH': 'math_result',
        'STRUC': 'struc_result',
        'ACRM': 'acrm_result',
        'PWRP': 'pwrp_result',
        'EEMLE': 'eemle_result',
    }

    subject_field_map_time = {
        'AERO': 'aero_time',
        'MATH': 'math_time',
        'STRUC': 'struc_time',
        'ACRM': 'acrm_time',
        'PWRP': 'pwrp_time',
        'EEMLE': 'eemle_time',
    }

    score = 0
    T_none = 0
    total = questions.count()
    results = []

    for question in questions:
        user_letter = request.POST.get(f'question_{question.id}')
        user_answer = getattr(question, f'option_{user_letter.lower()}') if user_letter else None
        is_correct = (user_letter == question.correct_answer)
        if is_correct:
            score += 1

        if user_letter is None:
            T_none += 1

        results.append({
            'question': question,
            'user_answer': user_answer,
            'user_letter': user_letter,
            'is_correct': is_correct,
        })

    if T_none is 50:
        results = []

    current_time = now()
    time_spent = current_time - localtime(exam_setting.date_time)

    total_seconds = int(time_spent.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    formatted_time_spent = f"{hours:02d}:{minutes:02d}"

    # Save the subject-specific score
    if getattr(exam_result, subject_field_map_result[subject], None) is None:
        setattr(exam_result, subject_field_map_result[subject], score)
        setattr(exam_result, subject_field_map_time[subject], formatted_time_spent)
        exam_result.save()

    score = getattr(exam_result, subject_field_map_result[subject])
    formatted_time_spent = getattr(exam_result, subject_field_map_time[subject])

    percentage = (score / total) * 100 if total > 0 else 0
    passed = score >= passing_score

    # Handle feedback form
    if request.method == 'POST' and request.POST.get('satisfaction'):
        satisfaction_map = {
            'Dissatisfied': 1,
            'Satisfied': 2,
            'Very Satisfied': 3,
        }
        satisfaction_text = request.POST.get('satisfaction')
        satisfaction = satisfaction_map.get(satisfaction_text, 2)
        comments = request.POST.get('feedback', '')

        # Try to update existing feedback or create new one
        feedback, created = UserFeedback.objects.get_or_create(student_id=student_id)

        setattr(feedback, f'{subject.lower()}_satisfaction', satisfaction)
        setattr(feedback, f'{subject.lower()}_comments', comments)
        feedback.save()

        messages.success(request, 'Thank you! Your result and feedback has been submitted.')
        return redirect('home')

    return render(request, 'exam_results.html', {
        'score': score,
        'total': total,
        'results': results,
        'subject': subject,
        'percentage': round(percentage, 2),
        'passed': passed,
        'time_spent': formatted_time_spent,
    })


def about_us_view(request):
    return render(request, 'about_us_template.html')