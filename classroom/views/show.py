from django.shortcuts import render,redirect
from django.db import connection
from classroom.models import displaydata
import datetime
from ..models import Course,fill
from django.core.paginator import Paginator
from time import time 

from django.db.models import Max
from datetime import datetime
from numpy.ma.core import ids
from django.contrib  import messages
from classroom.models import User,Attendances
from ..forms import UserForm
from django.contrib.auth.hashers import make_password
current_date = datetime.date(datetime.now())
now =datetime.now()
current_time = now.strftime("%H:%M:%S")

#affiche la liste de presence d'un seul etudiant
def showclass(request): 
    if request.user.is_authenticated:
        cursor =connection.cursor()
        cursor.execute("SELECT username,name,A.date,hour,statut FROM classroom_user U,classroom_attendances A, classroom_course C WHERE A.student_id=U.id and A.course_id=C.id and U.id="+str(request.user.id)+" order by A.date desc ")
        result = cursor.fetchall()
        context = {"displaydata":result,"value":1,"id":current_date}
        return render(request,"classroom/students/quiz_list.html",context)
    else:
        return render(request, 'classroom/home.html')

#affiche la liste de presence d'un seul etudiant suivant une periode
def list_attend(request):  
    if request.method =='POST':  
        date1 = request.POST['date1']
        date2 = request.POST['date2']
    current_user = request.user
    cursor =connection.cursor()
    cursor.execute("SELECT username,name,A.date,hour,statut FROM classroom_user U,classroom_attendances A, classroom_course C WHERE A.student_id=U.id and A.course_id=C.id and U.id="+str(request.user.id)+" and A.date>='"+str(date1)+"' and A.date<='"+str(date2)+"' order by A.date desc")
    result = cursor.fetchall()
    paginator = Paginator(result,per_page=10)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    context = {"displaydata":page_obj.object_list,"value":1,"id":current_date,'date':date1,'date2':date2 ,'paginator':paginator,'page_number':int(page_number)}
    return render(request,"classroom/students/list_attend.html",context)

#Affiche l'interface d'admin
def admin_show(request): 
    return render(request,"classroom/admin_p/admin.html")

def show_lecturer(request):  
    if request.user.is_authenticated:
        if request.user.is_teacher:
            current_user =request.user.id
            cursor =connection.cursor()
            cursor.execute("SELECT name,C.id FROM classroom_user U, classroom_course C WHERE U.id=C.lecturer_id  and U.id="+str(current_user)+"")
            result1 = cursor.fetchall() 
            cursor.execute("SELECT DISTINCT F.name,F.id_fill from classroom_user U,classroom_course C,classroom_fill F where U.id=C.lecturer_id and F.id_fill=C.fill_id and U.id="+str(current_user)+"")
            result2 = cursor.fetchall()
            
            context = {"displaydata":result1,'displaydata2':result2}
            return render(request,"classroom/teachers/index.html",context)
        else: 
            return render(request, 'classroom/home.html')   
    else:
        return render(request, 'classroom/home.html')
    
def save_attend(request):
    user_id_list =request.POST.getlist('user_id')
    remark_list =request.POST.getlist('remark')
    course_id=request.POST.get('course_id')
    fill_id=request.POST.get('fill_id')
    statut_value=0
    for remark in remark_list:
        user_id = user_id_list[remark_list.index(remark)]
        user_info_dict={'course_id':course_id,'student_id':remark,'statut':statut_value,'fill_id':fill_id,'date':current_date,'hour':current_time}
        if not Attendances.objects.filter(student_id=remark,date=current_date).exists():
                Attendances.objects.create(**user_info_dict)
        else : 
            messages.success(request,"You have already created a attendance list for this day")
            break
    return redirect('/')


def show_attendance(request):
    value =1
    if request.user.is_authenticated :
        course="null"
        fills="null"
        if request.method =='POST':  
            course= request.POST['course']
            fills= request.POST['fill']
            attend_value= Attendances.objects.filter(fill_id=fills,date=current_date,course_id=course)
            users=User.objects.filter(fill_id=fills)  
            fill_name =  fill.objects.get(id_fill=fills)
        context={'course':course, 'fill':fills,'userid':request.user.id,'users':users,'attend_value':attend_value,'value':value,'current_date':current_date,'fill_name':fill_name}
        return render(request,"classroom/teachers/test.html",context)
    else:
        return render(request, 'classroom/home.html')

def course(request):
   
    count1= Course.objects.all().count()
    course_value= Course.objects.all().order_by('-date')
    
    #paginator =Paginator(value2,per_page=10)
    #page_number = request.GET.get('page',1)
    #page_obj = paginator.get_page(page_number)
    
    lect_info=User.objects.filter(is_teacher=1)
    fill_value = fill.objects.all().order_by('-date')
    count2 = fill.objects.all().count()
    #paginator1=Paginator(value3,per_page=10)
    #page_number1 = request.GET.get('page',1)
    #page_obj1=paginator1.get_page(page_number1)
    context ={'lect_info':lect_info,'fill':fill_value,'fill_name':fill_value,'course':course_value,'count1':count1,'count2':count2}
    return render(request,"classroom/admin_p/course.html",context)


def listUser(request):  
    fill_name=fill.objects.all()
    count_User=User.objects.filter(is_student=True).count()
    listStudent= User.objects.filter(is_student=True).order_by('-date_joined')
    #paginator=Paginator(listStudent,per_page=10)
    #page_number=request.GET.get('page',1)
    #page_obj=paginator.get_page(page_number)
    
    
    context={'listStudent':listStudent,'fill_name':fill_name,'count1':count_User}    
    return render(request,"classroom/admin_p/list_user.html",context)

def updateStudent(request): 
    if request.method == 'POST':
        ids=request.POST['id']
        firstName= request.POST['firstName']
        lastName= request.POST['lastName']
        email= request.POST['email']
        fill_id=request.POST['fill']
        phoneNumber=request.POST['phoneNumber']
        User.objects.filter(id=ids).update(username=firstName,last_name=lastName,email=email,fill_id=fill_id,Phone_number=phoneNumber)
        return redirect('/admin/listUser')

def deleteStudent(request,id): 
    
    User.objects.filter(id=id).delete()
    return redirect('/admin/listUser')
def user(request):
    fill_name =fill.objects.all()
    max_id=User.objects.last()
    latest_val = max_id.id
    form =UserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            firstName = form.cleaned_data["firstName"]
            lastName=form.cleaned_data["lastName"]
            email=form.cleaned_data["email"]
            phoneNumber=form.cleaned_data["phoneNumber"]
            password =make_password(form.cleaned_data["password"])
            fill_id = request.POST["fill_id"]
            if(not User.objects.filter(email=email).exists()):
                users= User.objects.create(password=password,username=firstName,last_name=lastName,email=email,is_active=1,is_student=1,fill_id=fill_id,Phone_number=phoneNumber)
                if(users is not None ):
                    messages.success(request,"you record has been performed with success")
                    return redirect('/admin/user')
        else:
            return render(request,"classroom/admin_p/new_user.html",{'form':form,'fill_name':fill_name})   
            messages.error(request,"Verify please each field")
    context={'form':form,'users':user,'fill_name':fill_name,'max':latest_val}
    return render(request,"classroom/admin_p/new_user.html",context)

def add_course(request):  
    if request.method=="POST":
        code= request.POST['code']
        name=request.POST['name']
        time = request.POST['time']
        fill_id=request.POST['fill']
        lecturer_id=request.POST['lecturer_id']
        if not Course.objects.filter(course_code=code).exists():
            fills = fill.objects.get(id_fill=fill_id)
            Course.objects.create(course_code=code,name=name,time_allocated=time,fill=fills,lecturer_id=lecturer_id)
        return redirect('/admin/course')
    
def update_course(request):
    if request.method == 'POST':
        ids=request.POST['id']
        code= request.POST['code']
        name=request.POST['name']
        time = request.POST['time']
        fill_id=request.POST['fill']
        lecturer_id =request.POST['lecturer_id']
        fills = fill.objects.get(id_fill=fill_id)
        Course.objects.filter(id=ids).update(course_code=code,name=name,time_allocated=time,fill=fills,lecturer_id=lecturer_id)
        return redirect('/admin/course')
    
def delete_course(request,id):
    Course.objects.filter(id=id).delete()
    return redirect('/admin/course')

def update_fill(request):
    if request.method =='POST':  
        fill_id=request.POST['fill_id']
        fill_name=request.POST['fill_name']
        fill_desc=request.POST['desc']
        fill.objects.filter(id_fill=fill_id).update(name=fill_name,description=fill_desc)
        return redirect('/admin/course')

def delete_fill(request,id): 
    fill.objects.filter(id_fill=id).delete()
    return redirect('/admin/course')

def add_fill(request):  
    if request.method =='POST': 
        fills= request.POST['fill_names']
        fill_desc=request.POST['desc']
        if not fill.objects.filter(name=fills).exists():
            fill.objects.create(name=fills,description=fill_desc)
            messages.success(request,'Added with success')   

        else:
            messages.error(request,'this fill is already in database')   
        return redirect('/admin/course')