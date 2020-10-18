from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, User
from quiz.models import Quiz


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


def demo_login(request):
    demo_email = settings.DEMO_USER_EMAIL
    demo_pass = settings.DEMO_USER_PASS

    user = authenticate(username=demo_email, password=demo_pass)
    print(user)
    if user is not None:
        login(request, user)
        return redirect('/')

    elif user is None:
        messages.error(request, "Sorry! Demo login is not working at the moment.")
        return redirect('login')
 

class CustomLogoutView(LogoutView):
    template_name = 'quiz/home.html'


def user_create(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
    
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    stuff_for_frontend = {
        "user": request.user,
        "profile": request.user.profile,
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', stuff_for_frontend)


@login_required
def quiz_history(request):
    user = request.user
    profile = request.user.profile
    quizzes = Quiz.objects.filter(taken_by=user)

    context = {
        "quizzes": quizzes
    }

    return render(request, 'users/quiz_history.html', context)