from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from classroom.models import Course, Student, User, TakenCourse


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):

    email = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
            }
        ),
        label = "Email",
    )
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.email=self.cleaned_data.get('email')
        user.save()
        if commit:
            student = Student.objects.create(user=user)
            student.save()
            user.save()
        return user

class CourseAddForm(forms.ModelForm):
    course_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label = "*Course Title",
    )

    description = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label = "Add a little description",
        required = False,
    )
    class Meta:
        model = Course
        fields = ['course_name', 'description']

class GradeForm(forms.ModelForm):
    class Meta:
        model = TakenCourse
        fields = ('grade', )
        widgets = {
            'grade': forms.CheckboxSelectMultiple
        }
