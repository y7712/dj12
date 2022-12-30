from django.shortcuts import render,redirect
import googletrans
from googletrans import Translator

# Create your views here.
def trans(r):
    if r.user.is_anonymous:
        return redirect('acc:login')
    translator = Translator()
    l1=r.GET.get('oc','')
    o=r.GET.get('lang1','ko')
    tra=r.GET.get('lang2','en')
    context={
        "t":googletrans.LANGUAGES,
        "ol":o,
        'tl':tra
        }

    if l1:
        l2=translator.translate(l1, src=o, dest=tra).text
        context.update({
            "trcon":l2,
            "oricon":l1,
        })
    return render(r,'trans/trans.html',context)