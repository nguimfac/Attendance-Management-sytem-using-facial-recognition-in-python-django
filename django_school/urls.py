from django.urls import include, path
from django.contrib import admin
from classroom.views import classroom, students, teachers
from faceRecog import views as app_views

urlpatterns = [
    path('', include('classroom.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
    path('error_image$', app_views.errorImg),
    path('create_dataset', app_views.create_dataset),
    path('trainer', app_views.trainer),
    path('igen_train', app_views.eigenTrain),
    path('detect', app_views.detect),
    path('detect_image', app_views.detectImage),
]
