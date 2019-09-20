from django.shortcuts import render,redirect
from apps.login_app.models import *
from django.contrib import messages
import bcrypt
import datetime
from datetime import timedelta, timezone, tzinfo

# Create your views here.
def index(request):
    return render(request,"login_app/index.html")

def display_wall(request):
    messages =  Message.objects.all().order_by("-created_at")
    if messages:
        context = {
           "messages" : messages 
        }
    if 'userid' in request.session:
        context["user"] = User.objects.get(id=request.session['userid'])
        now = datetime.datetime.now()
        now_plus_30 = now + datetime.timedelta(minutes = 30)
        print("now_plus_30",now_plus_30)
        print("now",now)
        return render(request,"login_app/wall.html",context)
    else:
        return redirect('/')

def add_new_user(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        email = request.POST["email"]
        query_set = User.objects.filter(email = email)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
            if not query_set:
                new_user = User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password)
                #new_user = User.objects.create()
                # new_user valid to add in database
            else:
                print("not a new user")
                errors['email_exist'] = "Email exists! Please Login"
                #existing user redirect to Login page
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
            return redirect('/wall')

def post_message(request):
    if request.method == "POST":
        if 'userid' in request.session:
            this_user = User.objects.get(id=request.session['userid'])
            message = request.POST["message"]
            new = Message.objects.create(message=message,user=this_user)
            return redirect('/wall')
        else:
            return redirect('/')
            
def post_comment(request):
    if request.method == "POST":
        if 'userid' in request.session:
            this_user = User.objects.get(id=request.session['userid'])
            this_msg = Message.objects.get(id=request.POST["msg_id"])
            comment = request.POST["comment"]
            Comment.objects.create(comment=comment,user=this_user,message=this_msg)
            return redirect('/wall')
        else:
            return redirect('/')
        
def delete_msg(request):
    if request.method == "POST":
        msg_id = request.POST["msg_id"]
        this_msg =  Message.objects.get(id=msg_id)
        now = datetime.datetime.now(tz=timezone.utc)
        created_at_plus_30 = this_msg.created_at + datetime.timedelta(minutes = 30)
        print("now",datetime.datetime.now())
        print("created_at",this_msg.created_at)
        print(created_at_plus_30)
        if created_at_plus_30 > now :
            print(created_at_plus_30 ,"hello",now)
            this_msg.delete()
    return redirect('/wall')

        
def logout_user(request):
    request.session.flush()
    return redirect('/')




def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        errors = User.objects.basic_validator(request.POST)
        query_set = User.objects.filter(email = email)
        print(request.POST['password'].encode())
        # check that fields are not empty
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            if not query_set:
                # display please register 
                errors['email_not_exist'] = "Email doesn't exists! Please register"
                for key, value in errors.items():
                    messages.error(request, value)
                print("Not Existing User")
                return redirect('/')
            else:
                this_user = query_set[0]
                print(this_user.password)
                if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                    request.session['userid'] = this_user.id
                    print("logged User")
                    return redirect('/wall')
                else:
                    errors['invalid_password'] = "Invalid Password! Please check"
                    for key, value in errors.items():
                        messages.error(request, value)
                    print("Not Existing User")
                    return redirect('/')

        