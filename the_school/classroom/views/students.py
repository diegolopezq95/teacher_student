from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView
from ..forms import StudentSignUpForm
from ..models import Student, User, Course, TakenCourse
from django.contrib.auth.decorators import login_required
from ..decorators import student_required


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('student_list')

@login_required
@student_required
def StudentView(request):
    students = User.objects.filter(is_student=True)
    teachers = User.objects.filter(is_teacher=True)
    courses = Course.objects.all()
    taken_courses = TakenCourse.objects.filter(student__user=request.user)
    return render(request, 'students/student_list.html', {
        "students": students,
        "teachers": teachers,
        "courses": courses,
        "taken_courses": taken_courses,
        })

@login_required
@student_required
def allpeersView(request, course):
    students = User.objects.filter(is_student=False)
    teachers = User.objects.filter(is_teacher=True)
    courses = Course.objects.all() 
    taken_courses = TakenCourse.objects.filter(course__course_name=course)
    return render(request, 'students/classes/allclass.html', {
        "students": students,
        "teachers": teachers,
        "courses": courses,
        "taken_courses": taken_courses,
        })
