from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views import generic
from django.template.context_processors import csrf
from .models import user_signup,quiz_data,Question_data,option_data
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
# import mysql.connector
from django.contrib import messages
# Create your views here.


def login(request):
    if request.method == 'POST':
        sname = request.POST.get('username', '')
        spass = request.POST.get('password', '')
        user = auth.authenticate(username=sname,password=spass)
        if user is not None:
            # messages.success(request,"Login Successfull!!!")
            auth.login(request,user)
            return HttpResponseRedirect('/EasyToQuiz')
        else:
            messages.error(request,"Username or password invalid")
            return render(request,'login.html')
    else:
        return render(request, "login.html")

def userregistration(request):
    if request.method == 'POST':
        sname = request.POST.get('username', '')
        semail = request.POST.get('email', '')
        spass = request.POST.get('pass', '')
        spass1 = request.POST.get('cpass','')
        if spass==spass1:
            if User.objects.filter(username=sname).exists():
                messages.error(request,"username already exist.")
                return render(request, "userregistration.html")
            elif User.objects.filter(email=semail).exists():
                messages.error(request,"This email is already connected to an account.")
                return render(request, "userregistration.html")
            else:
                messages.success(request,"Register Successfull, please Login again for confirmation.")
                s = User.objects.create_user(username = sname, email=semail, password=spass)
                s.save()
                return HttpResponseRedirect('/EasyToQuiz/login')
        else:
            messages.error(request,"confirm password is not same as password! please check!")
            return render(request, "userregistration.html")
    else:
        return render(request, "userregistration.html")
def welcome(request):
    return render(request, "welcome.html")
    
def signout(request):
    logout(request)
    return redirect("EasyToQuiz")

def createquiz(request):
    return render(request, "createquiz.html")

def savingquiz(request):
    if request.method == 'POST':
        quiztitle=request.POST.get('title','')
        quizdescription=request.POST.get('description','')
        u_id =int(request.POST.get('u_id',''))
        q = quiz_data(quiztitle=quiztitle , description=quizdescription ,username_id=u_id)
        q.save()
        print(request.POST.get('x','')+"hi")
        array2=request.POST.get('array2','').split(",")
        array=request.POST.get('array','').split(",")
        print(array2)
        for i in range(0,int(request.POST.get('x',''))):
            if array2[i+1]=='1':
                questiontitle=request.POST.get('QuestionTitle-'+str(i+1),'')
                questiontype=False
                quizid=q.id
                Q = Question_data(qtitle=questiontitle,qtype=questiontype,quizid_id=quizid)
                Q.save()
                for j in range(1,int(array[i+1])+1):
                    option = request.POST.get("option-"+str(i+1)+"-"+str(j))
                    if option:
                        questionid=Q.id
                        op = option_data(option=option,questionid_id=questionid)
                        op.save()
        return HttpResponseRedirect('/EasyToQuiz/createquiz')

def quizdata(request):
    return render(request, "quizdata.html")

def quiz(request):
    return render(request, "quiz.html")