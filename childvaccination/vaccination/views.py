from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from vaccination.models import Userdetail
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'home.html')

def user_login(request):
    if request.method=="POST":
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('vaccination:home')
        else:
            messages.error(request,"Invalid Credentials")


    return render(request,'login.html')

def register(request):
    if request.method=="POST":
        u=request.POST['u']
        p=request.POST['pw']
        cp=request.POST['pw1']
        e=request.POST['e']
        fn=request.POST['fn']
        ln=request.POST['ln']
        ch=request.POST['role']

        if p==cp:
            user=User.objects.create_user(username=u,password=p,first_name=fn,last_name=ln,email=e)
            user.save()
            userdetail=Userdetail.objects.create(user=user,choice_field=ch)
            userdetail.save()
            return redirect('vaccination:home')
    return render(request,'register.html')


def about(request):
    return render(request,'about.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('vaccination:home')

