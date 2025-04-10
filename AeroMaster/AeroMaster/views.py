from django.shortcuts import render, redirect
from django.utils.timezone import localtime

from django.contrib.auth import login

from . import settings
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from AeroMaster_admin.models import ExamSetting, GeneratedQuestions


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


@user_required
def home_view(request):
    def get_exam(subject_code):
        try:
            exam = ExamSetting.objects.get(subject=subject_code)
            exam.date_time = localtime(exam.date_time)
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
    # Query the database to get all questions with the specific subject
    questions = GeneratedQuestions.objects.filter(subject=subject)
    if request.method == 'POST':
        score = 0
        total = questions.count()
        results = []

        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            is_correct = (user_answer == question.correct_answer)
            if is_correct:
                score += 1

            results.append({
                'question': question,
                'user_answer': user_answer,
                'is_correct': is_correct,
            })

        return render(request, 'exam_results.html', {
            'score': score,
            'total': total,
            'results': results,
            'subject': subject,
        })

    # Render the template and pass the questions data
    return render(request, 'exam.html', {'subject': subject, 'questions': questions})