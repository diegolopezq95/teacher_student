from django.db import models
from django.contrib.auth.models import AbstractUser


A = "A"
B = "B"
C = "C"
D = "D"
F = "F"

PASS = "PASS"
FAIL = "FAIL"

GRADE = (
		(A, 'A'),
		(B, 'B'),
		(C, 'C'),
		(D, 'D'),
		(F, 'F'),
	)

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='taken_course', on_delete=models.CASCADE)
    grade = models.CharField(choices=GRADE, max_length=1, blank=True)

    def get_comment(self, grade):
        if not grade == "F":
            comment = PASS
        else:
            comment = FAIL
        return comment

    def __str__(self):
        return '{} {} {}'.format(self.student, self.course, self.grade)