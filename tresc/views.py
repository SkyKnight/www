# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from tresc.models import *
from news.models import News
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def index(request, odnosnik):
    wpis = get_object_or_404(Strona, slug=odnosnik)
    wpisy = Strona.objects.all()
    news_glob = News.objects.filter(published=True).order_by('date').reverse()[:10]
    return render_to_response('static.html', RequestContext(request, {'wpis':wpis, 'wpisy':wpisy, 'news_glob':news_glob}))
#   return HttpResponse(u'wywołałeś z parametrem: "' + odnosnik + '"')

def links(request):
    l = Link.objects.all().order_by('weight')
    return render_to_response('links.html', RequestContext(request, {'l':l}))
