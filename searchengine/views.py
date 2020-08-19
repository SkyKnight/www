# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from news.models import News
from tresc.models import Strona
from django.db.models import Q
from django.views.generic.list_detail import object_list
# from pp.searchengine.web_search import google

def search(request):
    if 'q' in request.GET:
        term = request.GET['q']
        news = News.objects.reverse().filter(Q(text__contains=term)|Q(title__contains=term))
        pages = Strona.objects.reverse().filter(Q(tresc__contains=term)|Q(tytul__contains=term))
        news_glob = News.objects.all().order_by('date').reverse()[:10]
#    return object_list(
#                     request,
#                     news,
#                     extra_context = {"pages":pages},
#                     template_name = 'search_results.html')
    return render_to_response('search_results.html', {'term':term, 'news': news, 'pages':pages, 'news_glob':news_glob})

