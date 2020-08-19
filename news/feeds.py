#-*- coding: utf-8 -*-
from news.models import *
from django.contrib.syndication.feeds import Feed

class LatestNews(Feed):
    title = "Liturgia klasyczna w kościele NSPJ w Bydgoszczy. Informacje."
    link = "/"
    description = "Liturgia klasyczna w kościele NSPJ w Bydgoszczy. Informacje."
    def items(self):
        return News.objects.filter(published=True).order_by('date')

