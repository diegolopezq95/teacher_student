from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView
from ..forms import TeacherSignUpForm, GradeForm
from ..models import Student, User, Course, TakenCourse
from django.contrib.auth.decorators import login_required
from ..decorators import teacher_required
import sys


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teacher_list')

@login_required
@teacher_required
def TeachersView(request):
    no_students = Student.objects.all().count()
    students = User.objects.filter(is_student=False)
    teachers = User.objects.filter(is_teacher=True).count()
    courses = Course.objects.all()
    taken_courses = TakenCourse.objects.all()
    return render(request, 'teachers/teacher_list.html', {
        "students": students,
        "teachers": teachers,
        "courses": courses,
        "taken_courses": taken_courses
        })

@login_required
@teacher_required
def allcoursesView(request, course):
    students = User.objects.filter(is_student=False)
    teachers = User.objects.filter(is_teacher=True)
    courses = Course.objects.all() 
    taken_courses = TakenCourse.objects.filter(course__course_name=course)
    return render(request, 'teachers/classes/allclass.html', {
        "students": students,
        "teachers": teachers,
        "courses": courses,
        "taken_courses": taken_courses,
        })

@login_required
@teacher_required
def new_gradeView(request, course, pk):
    taken_course = TakenCourse.objects.filter(student_id=pk).filter(course__course_name=course)
    if request.method == 'POST' and request.POST.get('gradess'):
        form = GradeForm(request.POST)
        for taken in taken_course:
            if form.is_valid():
                TakenCourse.objects.filter(student_id=pk).filter(course__course_name=course).update(
                    grade = request.POST.get('gradess'),
                    student_id = pk,
                    course_id = taken.course_id
                )
                return redirect('update_grade', course, pk)
    else:
        form = GradeForm()
    return render(request, 'teachers/new_grade.html', {
        'taken_course': taken_course,
        'form': form,
        })