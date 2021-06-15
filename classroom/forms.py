from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.db import models
from classroom.models import (Answer, Question, Student, StudentAnswer,
                              Subject, User,fill)
class OrderFilter(forms.Form):
    search = forms.CharField(label="Search",help_text="Search there",widget=forms.TextInput(attrs={'class': 'form-control','placeholder':''}))
   

class UserForm(forms.Form):
    firstName = forms.CharField(label="FirstName",help_text="First Name",widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your firstName'}))
    lastName = forms.CharField(label="LastName",help_text="Last Name",widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your LastName'}))
    email = forms.EmailField(label="Email",help_text="Email",widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your Email'}))
    phoneNumber =forms.CharField(min_length=3,max_length=15,help_text="Phone Number",label="Phone Number",widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter your Phone number'}))
    password =forms.CharField(min_length=8,help_text="Password",label="Mot de passe ",widget =forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your Password'}))
    
class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
