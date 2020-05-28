from django.contrib import admin
from .models import Course, Student, User, TakenCourse

# Register your models here.
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(User)
admin.site.register(TakenCourse)