#-*- coding: utf-8 -*-
from django import forms 
from django.utils import simplejson
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext
from news.models import News
from tresc.models import Strona
from captcha.fields import CaptchaField
from contact.models import *
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def login(request):
    return HttpResponseRedirect('/admin')


class ContactForm1(forms.ModelForm):
    antySpam = CaptchaField(help_text=u"Proszę przepisac tekst z obrazka")
    class Meta:
        model=Contact
        exclude=['accord',]
    
    def __init__(self, *args, **kwargs):
        super(ContactForm1, self).__init__(*args, **kwargs)
        self.fields['adresat'].queryset = Adresat.objects.filter(visible=True)
        
class ContactForm(forms.Form):
    name = forms.CharField(help_text="Imię, Nazwisko Nadawcy")
    theme = forms.CharField(help_text="Temat", required=False)
    email = forms.EmailField(help_text="Adres email ...",required=True)
    message = forms.CharField(widget=forms.Textarea,required=True)
    cc_myself = forms.BooleanField(required=False)
    accord = forms.BooleanField(required=False)
    antySpam = CaptchaField()

def sendform(request):
    if request.method == 'POST':
        form = ContactForm1(request.POST)
        if form.is_valid():
            form.save() 
            data = form.cleaned_data
            adresat = data['adresat'].user.email
            email_body = u" Od: %s < %s >\n Wysłano za pomocą formularza kontaktowego ze strony www.nspj.bydgoszcz.pl\nTreść: \n %s \n " %( data['name'], data['email'], data['message'])
            #if data['accord']:
                #email_body = email_body + u"Nadawca wyraził zgodę na publikację"
            email = EmailMessage(data['theme'],
                                 email_body,
                                 to=[adresat,], headers={'From': data['email'],'Reply-To': data['email']})
            email.send()
            return HttpResponseRedirect('/kontakt/thanks')
        else:
            return render_to_response('contact.html', RequestContext(request, {'form': form}))
#            form = ContactForm()
    else:
        form = ContactForm1()
    news = News.objects.all().order_by('date').reverse()[:10]
    try:
        txt = Strona.objects.get(slug="kontakt").tresc
    except:
        txt = "Parafia NSPJ Bydgoszcz, pl. Piastowski 5"
    return render_to_response('contact.html', RequestContext(request, {'form': form, 'newsy': news, 'txt':txt,}))

def thanks(request):
    news = News.objects.all().order_by('date').reverse()[:10]
    return render_to_response('thanks.html', RequestContext(request, {'newsy': news,}))


@login_required
def listy(request):
    if request.user.groups.filter(name='biuro'):
        w = Q(adresat__user__email='biuro@nspj.bydgoszcz.pl')|Q(adresat__user__email=request.user.email)
    else:
        w = Q(adresat__user__email=request.user.email)    
    wszystkie = Contact.objects.filter(w).order_by('pk').reverse()
    return object_list(
        request,
        wszystkie,
        paginate_by = 50,
        template_name = 'listy.html')


    
@login_required
def odpowiedzi(request):
    wszystkie = Odpowiedz.objects.all().order_by('pk').reverse()
    return object_list(
        request,
        wszystkie,
        paginate_by = 30,
        template_name = 'odpowiedzi.html')
    
 
@login_required
def pokaz_odp(request,pk):
    l = Odpowiedz.objects.get(pk=pk)
    return render_to_response('odp.html', RequestContext(request, {'l':l}))
    

@login_required
def pokaz_list(request,pk):
    a = Adresat.objects.filter(visible=True)
    l = Contact.objects.get(pk=pk)
    return render_to_response('list.html', RequestContext(request, {'l':l, 'a':a}))

@login_required
def przekaz_list(request,pk,adresat):
    otrzymany = Contact.objects.get(pk=pk)
    adresat_ = Adresat.objects.get(pk=adresat)
    przekazany = Contact()
    przekazany.adresat = adresat_
    przekazany.name = otrzymany.name
    przekazany.theme = otrzymany.theme
    przekazany.email = otrzymany.email
    przekazany.message = otrzymany.message
    przekazany.cc_myself = otrzymany.cc_myself
    przekazany.accord = otrzymany.accord
    przekazany.date = otrzymany.date
    przekazany.save()
    email_body = otrzymany.message
    email = EmailMessage(otrzymany.theme,
            email_body,
            to=[adresat_.user.email, ], 
            headers={'From': 'biuro@nspj.bydgoszcz.pl','Reply-To':'biuro@nspj.bydgoszcz.pl'})
    email.send()
    naglowek = "List przekazano do " + adresat_.user.email + '\n\n' + '==================' + '\n\n'
    otrzymany.message = naglowek + otrzymany.message
    otrzymany.save()
    return render_to_response('list.html', RequestContext(request, {'l':otrzymany, 'm':'Przekazano'}))
    
@login_required
def odpowiedz(request, pk):
    list = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        form = OdpowiedzForm(request.POST)
        if form.is_valid():
            odp = form.save()
            odp.list = list
            odp.save()
            data = form.cleaned_data
            email_body = data['message']
            email = EmailMessage(data['theme'],
                                 email_body,
                                 to=[list.email, 'rak.odwaga@gmail.com'], headers={'From': 'biuro@nspj.bydgoszcz.pl','Reply-To':'biuro@nspj.bydgoszcz.pl'})
            email.send()
            return HttpResponseRedirect('/odpowiedz/thanks')
        else:
            return render_to_response('odpowiedz.html', RequestContext(request, {'form': form}))
#            form = ContactForm()
    else:
        re_theme = u"Odp: "+list.theme
        re_body = u"\n\n\n\n\n ---------- Oryginalny list: ----------\n"+list.message
        form = OdpowiedzForm({'theme':re_theme, 'message':re_body})

    return render_to_response('odpowiedz.html', RequestContext(request, {'form': form, "list":list}))

def thanks(request):
    news = News.objects.all().order_by('date').reverse()[:10]
    return render_to_response('thanks.html', RequestContext(request, {'newsy': news,}))
    
def thanks1(request):
    return render_to_response('thanks1.html', RequestContext(request, {}))

