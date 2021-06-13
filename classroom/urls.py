from django.urls import include, path
from django.contrib import admin
from .views import classroom, students, teachers,show
urlpatterns = [
      path('', classroom.home, name='home'),
      path('admin/', include(([
      path('', show.admin_show, name='admin'),
      path('course', show.course, name='course'),
      path('newStudent',show.user, name='user'),
      path('listUser',show.listUser,name='listUser'),
      path('user',show.user, name='user'),
      path('updateStudent',show.updateStudent,name='updateStudent'), 
      path('add_course',show.add_course, name='add_course'),
      path('update_course',show.update_course, name='update_course'),
      path('delete_course/<int:id>',show.delete_course,name='delete_course'),
      path('deleteStudent/<int:id>',show.deleteStudent,name='deleteStudent'),
      path('update_fills',show.update_fill, name='update_fill'),
      path('delete_fill/<int:id>',show.delete_fill,name='delete_fill'),
      path('add_fill',show.add_fill,name='add_fill')
    ], 'classroom'), namespace='admin')),

    
    path('', classroom.home, name='home'),
    path('students/', include(([
        path('', show.showclass, name='quiz_list'),
        path('show', show.list_attend, name='quiz_listing'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', show.show_lecturer, name='index'), 
        path('save_attend',show.save_attend, name='save_attend'),
        path('attendance',show.show_attendance,name='attendance'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
