from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages

# Create your views here.
def index(r):
    return render(r,'acc/index.html')

def ulogin(r):
    if r.user.is_authenticated:
        return redirect("acc:index")
    if r.method=="POST":
        un=r.POST.get('id')
        up=r.POST.get('pw')
        user=authenticate(username=un,password=up)
        if user:
            login(r,user)
            messages.success(r,f"{un}님 환영합니다.")
            return redirect('acc:index')
        else:
            messages.error(r,'없는 아이디 이거나 비밀번호가 틀립니다.')
    return render(r,'acc/login.html')

def signup(r):
    if r.user.is_authenticated:
        return redirect("acc:index")
    if r.method=="POST":
        un=r.POST.get('id')
        up=r.POST.get('pw')
        ucp=r.POST.get('cpw')
        p=r.FILES.get('up')
        cm=r.POST.get('com')
        try:
            if up==ucp:
                User.objects.create_user(username=un,password=up,comment=cm,pic=p)
                return redirect('acc:login')
        except:
            pass
    return render(r,'acc/signup.html')

def ulogout(r):
    logout(r)
    return redirect("acc:index")

def profile(r):
    if r.user.is_anonymous:
        return redirect("acc:login")
    return render(r,'acc/profile.html')

def update(r):
    if r.user.is_anonymous:
        return redirect("acc:login")
    if r.method=="POST":
        u=r.user
        ue=r.POST.get('em')
        uc=r.POST.get('com')
        p=r.FILES.get('up')
        if u.pic and p:
            u.pic.delete()
            u.pic=p
        u.email,u.comment=ue,uc
        u.save()
        return redirect('acc:profile')
    return render(r,'acc/update.html')

def delete(r):
    if r.method=="POST":
        ucp=r.POST.get('ch')
        up=r.user.password
        if check_password(ucp,up):
            r.user.pic.delete()
            r.user.delete()
    return redirect('acc:index')

def chpass(r):
    if r.user.is_anonymous:
        return redirect("acc:login")
    if r.method=="POST":
        ucp=r.POST.get('chp')
        up=r.user.password
        new=r.POST.get('np')
        if check_password(ucp,up):
            r.user.set_password(new)
            r.user.save()
            logout(r)
            return redirect('acc:index')
    return redirect('acc:update')