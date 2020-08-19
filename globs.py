# -*- coding: utf-8 -*-
#!/usr/bin/python
# TEMPLATE_CONTEXT_PROCESSOR
import datetime
from news.models import News, Block, Film, Slide

def globs(request):
    news_glob = News.objects.values('title','slug').filter(published=True).order_by('date').reverse()[:10]
    promo = Slide.objects.all()
    try:
        bodies = Block.objects.filter(published=True).order_by('date').reverse()
        block = Block.objects.filter(published=True).order_by('date').reverse()[0]
        body = block.body
        title = block.title 
    except:
        body = ""
        title = ""
    pol={
            1:u"styczeń",
            2:u"luty",
            3:u"marzec",
            4:u"kwiecień",
            5:u"maj",
            6:u"czerwiec",
            7:u"lipiec",
            8:u"sierpień",
            9:u"wrzesień",
            10:u"październik",
            11:u"listopad",
            12:u"grudzień"
            }
    ang={
            1:"jan",
            2:"feb",
            3:"mar",
            4:"apr",
            5:"may",
            6:"jun",
            7:"jul",
            8:"aug",
            9:"sep",
            10:"oct",
            11:"nov",
            12:"dec"
         }

    
    month_list = []
    for i in News.objects.filter(published=True).values('date'):
        month={'year':i['date'].year,'month':i['date'].month, 'pol':pol[i['date'].month], 'ang':ang[i['date'].month]}
        if month not in month_list:
            month_list.append(month)
    try:
        f=Film.objects.latest('date')
        film = f.youtube_url_id
    except:
        film = ''
    return {'news_glob': news_glob, 'promo':promo, 'month_list':month_list, 'title':title, 'bodies':bodies, 'film':film}

