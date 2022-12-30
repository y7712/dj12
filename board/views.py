from django.shortcuts import render,redirect
from .models import *
from django.utils import timezone
from django.core.paginator import Paginator
from acc.models import *

# Create your views here.
def index(r):
    if r.user.is_anonymous:
        return redirect('acc:login')
    pg=r.GET.get('page',1)
    cate=r.GET.get('cate',"")
    kw=r.GET.get('kw',"")
    if kw:
        if cate=='sub':
            b=Board.objects.filter(subject__contains=kw).order_by("-pubdate")
        elif cate=='wri':
            try:
                u=User.objects.get(username=kw)
                b=Board.objects.filter(writer=u).order_by("-pubdate")
            except:
                b=Board.objects.none()
        elif cate=='con':
            b=Board.objects.filter(content__contains=kw).order_by("-pubdate")
    else:
        b=Board.objects.all().order_by("-pubdate")
    cnt=b.count()
    pag=Paginator(b,5)
    obj=pag.get_page(pg)
    context={
        "bset":obj,
        'cate':cate,
        'kw':kw,
        'cnt':cnt,
    }
    return render(r,'board/index.html',context)

def detail(r,bpk):
    if r.user.is_anonymous:
        return redirect('acc:login')
    b=Board.objects.get(id=bpk)
    re=b.reply_set.all()
    context={
        'b':b,
        'rset':re,

    }
    return render(r,'board/detail.html',context)

def delete(r,bpk):
        b=Board.objects.get(id=bpk)
        if b.writer == r.user:
            b.delete()
            return redirect('board:index')
        else:
            pass
        return redirect('board:detail',bpk)
        

def create(r):
    if r.user.is_anonymous:
        return redirect('acc:login')
    if r.method=="POST":
        s=r.POST.get('sub')
        c=r.POST.get('con')
        Board(subject=s,content=c,pubdate=timezone.now(),writer=r.user).save()
        return redirect('board:index')
    return render(r,'board/create.html')

def update(r,bpk):
    if r.user.is_anonymous:
        return redirect('acc:login')
    b=Board.objects.get(id=bpk)
    context={
        "b":b
    }
    if b.writer == r.user:
        if r.method=="POST":
            s=r.POST.get('sub')
            c=r.POST.get('con')
            b.subject,b.content=s,c
            b.save()
            return redirect('board:detail',bpk)
    else:
        c=Board.objects.all()
        context={
            'bset':c
        }
        return render(r,'board/index.html',context)
    return render(r,'board/update.html',context)

def creply(r,bpk):
    if r.user.is_anonymous:
        return redirect('acc:login')
    b=Board.objects.get(id=bpk)
    re=r.POST.get('re')
    Reply(b=b,comment=re,replyer=r.user).save()
    return redirect('board:detail',bpk)

def dreply(r,bpk,rpk):
    re=Reply.objects.get(id=rpk)
    if r.user==re.replyer:
        re.delete()
    else:
        pass
    return redirect('board:detail',bpk)

def likey(r,bpk):
    if r.user.is_anonymous:
        return redirect('acc:login')
    b=Board.objects.get(id=bpk)
    if not r.user in b.likey.all():
        b.likey.add(r.user)
    else:
        b.likey.remove(r.user)
    return redirect('board:detail',bpk)
