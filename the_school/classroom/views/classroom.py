from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from ..models import Student, User, Course
from django.contrib.auth import login as auth_login


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher_list')
        else:
            return redirect('student_list')
    return render(request, 'classrooms/home.html')