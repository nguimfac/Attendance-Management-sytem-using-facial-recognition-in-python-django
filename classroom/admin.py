from django.contrib import admin
from .models import User,Student,Course,Attendances

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Attendances)
admin.site.register(Course)