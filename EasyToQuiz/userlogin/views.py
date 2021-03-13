from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views import generic
from django.template.context_processors import csrf
from .models import user_signup,quiz_data,Question_data,option_data,response_data
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages

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

def quiznext2(request):
    if request.method == 'POST':
        context = {"QuizID" : request.POST.get('QuizID','')}
        return render(request,"quiznext2.html",context)
    else:
         return HttpResponseRedirect('/EasyToQuiz')   

def savingquiz(request):
        if request.method == 'POST':
            quizid=0
        
            print(request.POST.get('save'))    
            quiztitle=request.POST.get('title','')
            quizdescription=request.POST.get('description','')
            u_id =int(request.POST.get('u_id',''))
            q = quiz_data(quiztitle=quiztitle , description=quizdescription ,username_id=u_id)
            q.save()
            array2=request.POST.get('array2','').split(",")
            array=request.POST.get('array','').split(",")
            for i in range(0,int(request.POST.get('x',''))):
                if array2[i+1]=='1':
                    questiontitle=request.POST.get('QuestionTitle-'+str(i+1),'')
                    questiontype=False
                    quizid=q.id
                    print(quizid)
                    Q = Question_data(qtitle=questiontitle,qtype=questiontype,quizid_id=quizid)
                    Q.save()
                    for j in range(1,int(array[i+1])+1):
                        option = request.POST.get("option-"+str(i+1)+"-"+str(j))
                        if option:
                            questionid=Q.id
                            op = option_data(option=option,questionid_id=questionid,quizid_id=quizid)
                            op.save()
            context = {"QuizID" : quizid }
            return render(request, "quiznext.html",context)

        else:
            return HttpResponseRedirect('/EasyToQuiz')

def quizdata(request):
    return render(request, "quizdata.html")

def quiz(request):
    if request.method == 'POST':
        user_id=request.POST.get('user_id','')
        quizid=request.POST.get('quizcode','')
        x = quiz_data.objects.raw("SELECT * from userlogin_quiz_data WHERE id=%s", [quizid])
        if len(x)==1:
            exist = response_data.objects.raw("SELECT * from userlogin_response_data WHERE userid_id=%s and quizid_id=%s", [user_id, quizid])
            if len(exist)!=0:
                return render(request, "submitquiz.html")
            Q_data=Question_data()
            for y in x:
                title=y.quiztitle
                discription=y.description
            questions = Question_data.objects.raw("SELECT * from userlogin_question_data WHERE quizid_id=%s", [quizid])
            option = option_data.objects.raw("SELECT * from userlogin_option_data WHERE quizid_id=%s", [quizid])
            print(type(questions))
            context = {"questions":questions , "options":option, "title":title, "description": discription}
            return render(request, "quiz.html",context)
        else:
            context = {"mymessage":"No Quiz available for this ID" }
            return render(request, "quizdata.html",context)
    else:
        return HttpResponseRedirect('/EasyToQuiz')

def submit(request):
    if request.method == 'POST':
        quizid=request.POST.get('quiz_id','')
        questions = Question_data.objects.raw("SELECT * from userlogin_question_data WHERE quizid_id=%s", [quizid])
        userid = int(request.POST.get('u_id',''))
        for question in questions:
            selected_option=request.POST.get('answer'+str(question.id),'1')
            qid=question.id
            response = response_data( answer_id=selected_option, questionid_id=qid, quizid_id=quizid, userid_id=userid)
            response.save()
        return render(request, "submitquiz.html")
    else:
        return HttpResponseRedirect('/EasyToQuiz')

def btw_submit(request):
    if request.method == 'POST':
        return render(request,"submit.html")
    else:
         return HttpResponseRedirect('/EasyToQuiz') 

def responses(request):
    return render(request,"responses.html")

def responses_data(request):
    quizid=request.POST.get("quizcode","")
    userid=request.POST.get("user_id","")
    quiz=quiz_data.objects.raw("SELECT * from userlogin_quiz_data WHERE id=%s and username_id=%s", [quizid,userid])
    if len(quiz)==1:
        responses=response_data.objects.raw("SELECT * from userlogin_response_data WHERE quizid_id=%s",[quizid])
        unique_username_list=[]
        for response in responses:
            # if response.userid_id!=userid:
            user1=User.objects.raw("SELECT DISTINCT * from auth_user WHERE id=%s",[response.userid_id])
            for x in user1:
                if x.id!=int(userid):
                    if x not in unique_username_list:
                        unique_username_list.append(x)
        context = {"responses":responses , "username_list":unique_username_list , "quizid":quizid}
        return render(request, "responses_data.html",context)
    else:
        context = {"mymessage":"Please enter valid Quiz id or this Quiz does not belong to you" }
        return render(request, "responses.html",context)
        
def view_response(request):
    username=request.POST.get("username","")
    user1=User.objects.raw("SELECT * from auth_user WHERE username=%s",[username])
    quizid=(request.POST.get("quizid",""))
    quiz=quiz_data.objects.raw("SELECT * from userlogin_quiz_data WHERE id=%s", [quizid])
    correct_answer_list=[]
    userid=quiz[0].username_id
    correct_response=response_data.objects.raw("SELECT * from userlogin_response_data WHERE quizid_id=%s and userid_id=%s",[quizid,userid])
    for cr in correct_response:
        correct_option=option_data.objects.raw("SELECT * from userlogin_option_data Where id=%s",[cr.answer_id])
        correct_answer_list.append(correct_option[0].option)
    responses=response_data.objects.raw("SELECT * from userlogin_response_data WHERE quizid_id=%s and userid_id=%s",[quizid,user1[0].id])
    
    question_list=[]
    answer_list=[]
    
    for response in responses:
        ques=Question_data.objects.raw("SELECT * from userlogin_question_data WHERE id=%s",[response.questionid_id])
        question_list.append(ques[0])
        answer=option_data.objects.raw("SELECT * from userlogin_option_data WHERE id=%s",[response.answer_id])    
        answer_list.append(answer[0])
    is_answerd=True
    i=0
    if len(correct_response)!=0:
        is_answerd=True
        response_list=zip(question_list,answer_list,correct_answer_list)
        for question,answer,correct_answer in response_list:
            if answer.option==correct_answer:
                i+=1
        response_list=zip(question_list,answer_list,correct_answer_list)
    else:
        is_answerd=False
        response_list=zip(question_list,answer_list)
    x=len(question_list)
    context={"response_list":response_list , "quiz":quiz[0], "total":x , "correct":i,"name":username,"email":user1[0].email, "answered":is_answerd}
    return render(request,"view_response.html",context)