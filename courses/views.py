from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Course


def home(request):
    courses = Course.objects.all()

    return render(request, 'courses/home.html', {
        'courses': courses
    })


def courses_list(request):
    courses = Course.objects.all()

    return render(request, 'courses/courses.html', {
        'courses': courses
    })


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    return render(request, 'courses/course_detail.html', {
        'course': course
    })


# REGISTER

def register(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Бош талааларды текшерүү
        if not name or not email or not password or not password2:
            messages.error(
                request,
                'Бардык керектүү талааларды толтуруңуз.'
            )
            return redirect('register')

        # Пароль текшерүү
        if password != password2:
            messages.error(
                request,
                'Паролдор дал келген жок.'
            )
            return redirect('register')

        # Email текшерүү
        if User.objects.filter(username=email).exists():
            messages.error(
                request,
                'Бул email менен аккаунт мурунтан бар.'
            )
            return redirect('register')

        # User түзүү
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        # Автоматтык login
        login(request, user)

        messages.success(
            request,
            'Каттоо ийгиликтүү аяктады!'
        )

        return redirect('profile')

    return render(request, 'register.html')


# LOGIN

def login_view(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('profile')

        messages.error(
            request,
            'Email же пароль туура эмес.'
        )

    return render(request, 'login.html')


# LOGOUT

def logout_view(request):

    logout(request)

    return redirect('home')


# PROFILE

def profile(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'profile.html')