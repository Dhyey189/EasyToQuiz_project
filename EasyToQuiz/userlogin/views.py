from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views import generic
from django.template.context_processors import csrf
from .models import user_signup
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
# import mysql.connector
from django.contrib import messages
# Create your views here.
def welcome(request):
    return render(request, "welcome.html")
def login(request):
    if request.method == 'POST':
        sname = request.POST.get('username', '')
        spass = request.POST.get('password', '')
        user = auth.authenticate(username=sname,password=spass)
        if user is not None:
            # messages.success(request,"Login Successfull!!!")
            auth.login(request,user)
            return render(request, "welcome.html")
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

def signout(request):
    logout(request)
    return redirect("EasyToQuiz")

def createquiz(request):
    return render(request, "createquiz.html")