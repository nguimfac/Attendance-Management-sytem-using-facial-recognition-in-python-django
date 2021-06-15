from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator 
from MySQLdb.constants.ER import AUTO_INCREMENT_CONFLICT


class displaydata(models.Model):
    Sname=models.CharField(max_length=100)
    Cname=models.CharField(max_length=100)
    
class fill(models.Model):
    id_fill= models.IntegerField(primary_key=True)
    name= models.CharField(max_length=155)
    description =models.CharField(max_length=500,default="Cette filière est destine a des persones tres intelligent et travailleur car il sagit bien d la filière software engineering")   
    date=models.DateField(default="2021-09-03")


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    fill=models.ForeignKey(fill, on_delete=models.CASCADE,default=1)
    Phone_number = models.IntegerField(default=659994937)
    activity = models.CharField(max_length=200, default=None)
class faceInfo(models.Model):  
    faceid=models.AutoField(primary_key=True)
    user =models.ForeignKey(User, on_delete=models.CASCADE,unique=True)
    
class Course(models.Model):
    course_code=models.CharField(max_length=100)
    name= models.CharField(max_length=50)
    time_allocated=models.PositiveIntegerField(default=0,validators=[MinValueValidator(1),MaxValueValidator(100)])
    fill=models.ForeignKey(fill, on_delete=models.CASCADE)
    date =models.DateField(default="2021-02-12")
    lecturer= models.ForeignKey(User, on_delete=models.CASCADE,default=6)
    
class Attendances(models.Model):
    date=models.DateField(default="2021-02-03")
    hour= models.TimeField(default="12:41:30")
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    statut = models.BooleanField(default=False)
    fill=models.ForeignKey(fill, on_delete=models.CASCADE,default=2)

class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
