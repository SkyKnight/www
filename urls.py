import os.path
import tagging
from django.conf.urls.defaults import *
from django.contrib import admin
from news.models import News
from news.feeds import *
from contact.views import ContactForm
from django.conf import settings

feeds = {'news': LatestNews,}

admin.autodiscover()

news_info = {
            "queryset"   : News.objects.exclude(status="B").exclude(status="G"),
            "date_field" : "date",
            "template_name"   : "archive.html" 
            }


urlpatterns = patterns('',
   (r'^admin/', include(admin.site.urls)),
#   (r'^admin/(.*)', admin.site.root),
   (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}),
#   (r'^site_media/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
   (r'^kontakt/$','contact.views.sendform' ),
   (r'^kontakt/thanks/$','contact.views.thanks'),
   (r'^odpowiedz/thanks/$','contact.views.thanks1'),
   (r'^listy/$','contact.views.listy' ),
   (r'^odpowiedzi/$','contact.views.odpowiedzi' ),
   (r'^list/(?P<pk>\d+)/$','contact.views.pokaz_list' ),
   (r'^list/przekaz/(?P<pk>\d+)/(?P<adresat>\d+)/$','contact.views.przekaz_list' ),
   (r'^film/$', 'news.views.film'),
   (r'^kazanie/$', 'news.views.kazanie'),
   (r'^katecheza/$', 'news.views.katecheza'),
   (r'^news/(?P<slug>[\w\-_]+)/$', 'news.views.show_news'),
   (r'^print/(?P<slug>[\w\-_]+)/$', 'news.views.print_news'),
#   (r'^ajax/$', 'news.views.ajax'),
#   (r'^(?P<slug>[\w\-_]+)/$', 'news.views.news_by_category'),
   (r'^/?$', 'news.views.index'),
   (r'^static/sitemap', 'news.views.sitemap'),
   (r'^static/', include('tresc.urls')),
   (r'^resp/', include('odpowiedzi.urls')), 
   (r'^tag/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', dict(queryset_or_model=News.objects.all().order_by('date').reverse())),
   (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
   (r'^search/?$', 'searchengine.views.search'),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'django.views.generic.date_based.archive_month', news_info),
   (r'^newsletter/subscribe/', 'newsletter.views.subscribe'),
   (r'^newsletter/unsubscribe/', 'newsletter.views.unsubscribe'),
   (r'^newsletter/sending/$', 'newsletter.views.sending'),
   (r'^regiony/(?P<region>[\w\-_]+)/$', 'news.views.regiony'),
   (r'^links/', 'tresc.views.links'),
   (r'^intencje/', 'intencje.views.index'),
   (r'^captcha/', include('captcha.urls')),
   (r'^odpowiedz/(?P<pk>\d+)/$','contact.views.odpowiedz' ),
   (r'^odpowiedz/zobacz/(?P<pk>\d+)/$','contact.views.pokaz_odp' ),
   (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
     
   
#   (r'^grappelli/', include('grappelli.urls')),
#   (r'^kontakt/$', 'django.views.generic.simple.direct_to_template', {'template':'contact.html','extra_context':{'f':ContactForm()}}),
#   (r'^kontakt/$','pp.contact.views.sendform' ),
)
