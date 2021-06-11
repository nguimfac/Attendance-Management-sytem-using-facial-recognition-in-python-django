from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:index')
        elif request.user.is_student:
            return redirect('students:quiz_list')
        else:
            return redirect('admin:admin')
    return render(request, 'classroom/home.html')
