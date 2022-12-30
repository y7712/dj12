from django.shortcuts import render,redirect
from PIL import Image
import random
from django.contrib import messages

# Create your views here.
def index(r):
    if r.user.is_anonymous:
        return redirect('acc:login')
    context={

    }
    if r.method=='POST':
        w=r.POST.get('wi')
        h=r.POST.get('hi')
        bw=r.POST.get('bw')
        p=r.FILES.get('ph')
        if p:
            if w or h or bw:
                img=Image.open(p)
                pn=p.name.split('.')
                ex=pn[len(pn)-1]
                si=img.size
                if not ex in ['jpg','png','jpeg']:
                    messages.error(r,"JPG,PNG,JPEG 파일만 업로드 할 수 있습니다.")
                    return redirect('imgcnv:index')
                if not w:
                    w=si[0]
                else:
                    w=int(w.lstrip('0'))
                if not h:
                    h=si[1]
                else:
                    h=int(h.lstrip('0'))
                p_name=p.name.split('.')[0]
                r1=""
                r2=""
                for i in range(0,random.randint(10,21)):
                    r1+=random.choice('abcdefghijklmnopqrstuvwxyz123456789')
                    r2+=random.choice('abcdefghijklmnopqrstuvwxyz123456789')
                img.save(f'media/cnvb/{p_name}_{r1}.{ex}')
                reimg=img.resize((w,h))
                if bw:
                    reimg=reimg.convert('L')
                reimg.save(f'media/cnva/{p_name}_{r2}.{ex}')
                context.update({
                    'r1':r1,
                    'r2':r2,
                    'n':p_name,
                    'ex':ex,
                    's':img.size
                })
            else:
                messages.info(r,'이미지에 변경사항이 없습니다.')
        else:
            messages.error(r,"파일을 넣어주세요.")
    return render(r,'imgcnv/index.html',context)
