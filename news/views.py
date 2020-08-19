# -*- coding: utf-8 -*-
from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from news.models import *

def index(request):
    
    news = News.objects.filter(published=True).order_by('date').reverse()
#    block = Block.objects.filter(published=True).order_by('date').reverse()[0]
    return object_list(
	request,
        news,
        paginate_by = 7,
        extra_context = {'main':1},
        template_name = 'index.html')

def news_by_category(request, slug):
	c = Category.objects.get(slug=slug)
	#news = News.objects.filter(category=c).order_by('-id')
	news = c.news_set.all()
	return object_list(
		request,
		news,
		paginate_by = 5,
		extra_context = {'c':c},
		template_name = 'news_by_category.html')

class AddCommentForm(forms.ModelForm):
	class Meta:
		model = Comment

def show_news(request, slug):
	try:
		news = News.objects.get(slug=slug)
	except:
		return render_to_response('error.html',
			{'error': 'Strona nie istnieje'},
			context_instance=RequestContext(request))
	if request.POST:
		data = request.POST.copy()
		data['news'] = news.id
		data['date'] = datetime.datetime.now()
		form = AddCommentForm(data)
		if form.is_valid():
			form.save()
	form = AddCommentForm()
	return render_to_response('show_news.html', {'news': news, 'form':form}, context_instance=RequestContext(request))


def print_news(request, slug):
        try:
                news = News.objects.get(slug=slug)
        except:
                return render_to_response('error.html',
                        {'error': 'Strona nie istnieje'},
                        context_instance=RequestContext(request))

        return render_to_response('print_news.html', {'news': news}, context_instance=RequestContext(request))



def kazanie(request):
    yt_url_id = request.GET.get('y', 'none')
    films = Kazanie.objects.all().exclude(youtube_url_id=yt_url_id)
    big_film = Kazanie.objects.filter(youtube_url_id=yt_url_id)
        
    try:
      if yt_url_id != 'none':
          Kazanie.objects.get(youtube_url_id=yt_url_id)
      return object_list(
            request,
            films,
            paginate_by = 5,
            extra_context = {"yt_url_id":yt_url_id, "big_film":big_film},
            template_name = 'kazania.html')
    except Exception, e:
#      return HttpResponse('brak:' + str(e))
      raise Http404


def katecheza(request):
    yt_url_id = request.GET.get('y', 'none')
    films = Katecheza.objects.all().exclude(youtube_url_id=yt_url_id)
    big_film = Katecheza.objects.filter(youtube_url_id=yt_url_id)
        
    try:
      if yt_url_id != 'none':
          Katecheza.objects.get(youtube_url_id=yt_url_id)
      return object_list(
            request,
            films,
            paginate_by = 5,
            extra_context = {"yt_url_id":yt_url_id, "big_film":big_film},
            template_name = 'kazania.html')
    except Exception, e:
#      return HttpResponse('brak:' + str(e))
      raise Http404

def film(request):
    yt_url_id = request.GET.get('y', 'none')
    films = Film.objects.all().exclude(youtube_url_id=yt_url_id)
    big_film = Film.objects.filter(youtube_url_id=yt_url_id)

    try:
      if yt_url_id != 'none':
          Film.objects.get(youtube_url_id=yt_url_id)
      return object_list(
            request,
            films,
            paginate_by = 5,
            extra_context = {"yt_url_id":yt_url_id, "big_film":big_film},
            template_name = 'films.html')
    except:
      raise Http404


def sitemap(request):
    news = News.objects.all().order_by('date').reverse()
    return render_to_response('sitemap.html', {'newsy':news})


def regiony(request, region):
    news = News.objects.filter(owner__profile__region__name=region).order_by('date').reverse()
    try:
        page = Region.objects.filter(name=region).values('page')[0]
    except:
        raise Http404
    return object_list(
        request,
        news,
        paginate_by = 5,
        extra_context = page,
        template_name = 'index_reg.html')

def testy(request):
    return HttpResponse('OK')
