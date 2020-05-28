from django.urls import include, path
from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),
    path('students/', include(([
        path('', students.StudentView, name='student_list'),
        path('all_class/<course>', students.allpeersView, name='all_class'),
        ]))),
    path('teachers/', include(([
        path('', teachers.TeachersView, name='teacher_list'),
        path('update_grade/<course>', teachers.allcoursesView, name='new_class'),
        path('update_grade/<course>/<pk>', teachers.new_gradeView, name='update_grade'),
    ])))
]