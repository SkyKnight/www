# -*- coding: utf-8 -*-
# Create your views here.

from newsletter.models import *
from django.template.loader import get_template
from django.views.generic.simple import redirect_to
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template import RequestContext
import datetime
import subprocess
import random

def gen_code():
    code = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890') for i in range(10)])
    return code

def subscribe(request):
    if not request.POST:
        return redirect_to(request, url='/') 
    email = request.POST['email']
    mlist = [].append(email)
    code = gen_code()
    subscription_date = datetime.datetime.now()
    subscr = Subscriber(email=email, code=code, subscription_date=subscription_date)
    subscr.save()
#    body=u"""Otrzymałeś ten list, ponieważ na stronie www.nspj.bydgoszcz.pl podano Twój adres do wysyłki newslettera. Jeśli chcesz otrzymywać newsletter kliknij na link lub wklej poniższy adres do przeglądarki, żeby potwierdzić subskrypcję.Jeśli nie wpisywałeś swojego adresu po prostu wykasuj ten mail. \n""" 
#    body = body + "http://www.nspj.bydgoszcz.pl/newsletter/accept/?code=" + code
#    send_mail("Newsletter ze strony pjn-kujawskopomorskie.pl",
#              body,
#              'biuro@nspj.bydgoszcz.pl',
#              mlist
#              )
    komunikat = u"""Dziękujemy za wpisanie adresu. Newsletter będzie wysyłany na adres """ + email
    
    return render_to_response('subscribed.html', RequestContext(request, {"komunikat":komunikat} ))

def unsubscribe(request):
    if not request.GET['email']:
        return redirect_to(request, url='/')
    email = request.GET['email']
    subscr = Subscriber.objects.filter(email=email)
    n = subscr.count()
    for s in subscr:
        s.delete()
    if n:
        komunikat = u"""Adres """ + email + u" został usunięty z naszej listy wysyłkowej."
    else:
        komunikat = u"""Adresu """ + email + u" nie było na naszej liście!"

    return render_to_response('subscribed.html', {"komunikat":komunikat} )

def make_html():
    from news.models import Newslet, News
    from django.template import Context
    from django.template.loader import get_template
    from datetime import datetime
    latest_newsletter = Newslet.objects.all().order_by('date').reverse()[0]
    t = get_template('newslet.html')
    news = News.objects.filter(newslet = latest_newsletter) 
    html = t.render(Context({"news":news, "date":datetime.now()}))
    t = get_template('newslet.txt')
    txt = t.render(Context({"news":news, "date":datetime.now()}))
    return {'txt':txt, 'html':html, 'unsent':latest_newsletter.unsent}
       
    


def sending(request):
    if request.user.is_superuser:
        link = "http://pjn-kujawskopomorskie.pl/newsletter/unsubscribe/?email="
        napis = u"Otrzymałeś ten biuletyn, ponieważ Twój ares e-mail został podany na stronie www.polska-plus.pl. Jeśli nie chcesz otrzymywac biuletynu, możesz usunąć swój adres, korzystając z następującego linku: "
#        adresy = Subscriber.objects.all()
        adresy = Probne.objects.all()
#        tresc_txt = Body.objects.all().order_by('sending_date').reverse()[0].text
#        tresc_html = Body.objects.all().order_by('sending_date').reverse()[0].text_html
        tresc = make_html()
        tresc_txt = tresc['txt']
        tresc_html = tresc['html']
        subject = u"Newsletter portalu pjn-kujawskopomorskie.pl"
        from_email = "biuro@walkowiak.bydgoszcz.pl"
        wszystkie = 0
        bledy = 0
#        return HttpResponse(u"Newsletter zaczyna się wysyłać, treść poniżej:<br />" + tresc_html)
        for a in adresy:
            cale = napis + '<a href="' + link + a.email + '">' + link + a.email + '</a>'
            txt = tresc_txt + '\n' + cale
            htm = tresc_html + '<p> </p><p>' + cale + '</p>'
            htm = '<link rel="stylesheet" type="text/css" media="screen" href="http://pjn-kujawskopomorskie.pl/site_media/themes/plus_1/style.css" />' + htm
            bledy_opis = ""
            try:
                msg = EmailMultiAlternatives(subject, txt, from_email, [a.email,])
                msg.attach_alternative(htm, "text/html")
                msg.send()
                wszystkie = wszystkie + 1
            except:
                pass
                bledy = bledy+1
                bledy_opis=bledy_opis + a.email + ", "
                
        return HttpResponse(u"Newsletter wysłany :) maili: " + str(wszystkie) + u", błędów: " + str(bledy) + u"<br /> błędy: " + bledy_opis )
    else:
        return HttpResponse(u"Nie jesteś adminem")


