from django.shortcuts import render,redirect
from acc.models import *
from .models import *

# Create your views here.
def index(r):
    if r.user.is_anonymous:
        return redirect('acc:login')
    t=Topic.objects.all()
    context={
        "tset":t
    }
    return render(r,'vote/index.html',context)

def detail(r,tpk):
    if r.user.is_anonymous:
        return redirect('acc:login')
    t=Topic.objects.get(id=tpk)
    c=t.choice_set.all()
    context={
        "t":t,
        "c":c
    }
    return render(r,'vote/detail.html',context)

def vote(r,tpk):
    if r.user.is_anonymous:
        return redirect('acc:login')
    t=Topic.objects.get(id=tpk)
    if not r.user in t.voter.all():
        t.voter.add(r.user)
        cpk=r.POST.get('sel')
        c=Choice.objects.get(id=cpk)
        c.choicer.add(r.user)
    else:
        t.voter.remove(r.user)
        r.user.choice_set.get(top=t).choicer.remove(r.user)
    return redirect('vote:detail',tpk)

def create(r):
    if r.user.is_anonymous:
        return redirect('acc:login')
    if r.method=="POST":
        s=r.POST.get('sub')
        con=r.POST.get('con')
        c_name=r.POST.getlist('na')
        c_com=r.POST.getlist('com')
        t=Topic(subject=s,maker=r.user,content=con)
        t.save()
        for i,j in zip(c_name,c_com):
            Choice(top=t,name=i,comment=j).save()
        return redirect('vote:index')
    return render(r,'vote/create.html')

def delete(r,tpk):
    t=Topic.objects.get(id=tpk)
    if r.user == t.maker:
        t.delete()
    else:
        pass
    return redirect('vote:index')