# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink
from django.contrib import admin
from fields import ThumbnailImageField
from markdown import markdown
import datetime
from tagging.fields import TagField
from tagging.models import Tag
import tagging
from django.contrib.auth.models import User
from django.core.files import File
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


def validate_prob(value):
    if value == 'Z':
        raise ValidationError(u'Tylko X. Prałat może zatwierdzać ogłoszenia')
#class Category(models.Model):
#    name = models.CharField(max_length=255, verbose_name='Nazwa Kategorii')
#    slug = models.SlugField(max_length=255, unique=True, verbose_name='Odnośnik')
#    icon =  models.ImageField(upload_to='icons', verbose_name='Ikonka Kategorii', blank=True)
#    class Meta:
#        verbose_name = "Kategoria"
#        verbose_name_plural = "Kategorie"
#    def __unicode__(self):
#        return self.name

class Newslet(models.Model):
    date = models.DateTimeField(verbose_name='Data przewidywana')
    sent_date =  models.DateTimeField(verbose_name='Data wysyłki', blank=True, null=True, editable=False)
    unsent = models.BooleanField(default=True, verbose_name='Niewysłany')
    report = models.CharField(max_length=255, verbose_name='Raport', blank=True, editable=False)
    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newslettery"
        ordering = ['-date']
    def __unicode__(self):
        return str(self.date)


class News(models.Model):
    STATUS = (
        ('B', u'Brudnopis'),
        ('G', u'Gotowe do zatwierdzenia'),
        ('Z', u'Zatwierdzone do publikacji'),
        ('A', u'Archiwalne')
    )

#    category = models.ManyToManyField(Category, verbose_name='Kategorie')
    title = models.CharField(max_length=255, verbose_name='Tytuł')
    title_short = models.CharField(max_length=25, verbose_name='Krótki tytuł (na slajd)', blank=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Odnośnik')
    text_markdown = models.TextField(verbose_name='Treść')
    text_short = models.CharField(max_length=100, verbose_name='Krótka treść (na slajd)', blank=True)
    text = models.TextField(editable=False)
    date = models.DateTimeField(verbose_name='Data dodania')
    promoted = models.BooleanField(verbose_name='Promowany w pokazie slajdów')
    tags = TagField()
    owner = models.ForeignKey(User, verbose_name='Kto wpisał')
    published = models.BooleanField(verbose_name='Na str. główną')
    newslet = models.ForeignKey(Newslet, blank=True, null=True, verbose_name='Newsletter')
    status = models.CharField(max_length=10, choices=STATUS)
    def _words(self):
        import re
        k=0
        l = self.text_markdown
        p = re.compile(r'<.*?>')
        l = p.sub('', l)
        l = l.split(' ')
        for i in l:
            k=k+1
        return k

    words = property(_words)

    def _trunc(self):
        if self.words > 45:
            return True
        else:
            return False

    trunc = property(_trunc)        

    class Meta:
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"
        ordering = ['-date']

    def __unicode__(self):
        return self.title
	
    def get_absolute_url(self):
	    return '/news/' + self.slug + '/'

    

    def save (self):
        self.text = markdown(self.text_markdown)
        if self.status == 'Z': 
            self.status = 'B'
        if self.status == 'G':
            txt="Ksiądz wikariusz prosi o zatwierdzenie ogłoszeń"
            try:
                msg = EmailMultiAlternatives("ogłoszenia przygotowane", txt, 'admin@nspj.bydgoszcz.pl', ['rak.odwaga@gmail.com', 'michal@jedryka.com'])
                msg.attach_alternative(txt, "text/html")
                msg.send()
            except:
                pass

            
        super(News, self).save()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)      


class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name="wojewodztwo")
    page = models.TextField(verbose_name='Strona z opisem')
    def __unicode__(self):
        return self.name


class Profile(models.Model):
    person = models.OneToOneField(User)
    region = models.ForeignKey(Region)
    def __unicode__(self):
        return self.person.username
                            

class Comment(models.Model):
    news = models.ForeignKey(News, verbose_name='Wiadomość')
    author = models.CharField(max_length=50, verbose_name='Autor - nazwisko lub pseudonim')
    e_mail = models.EmailField(blank=True, verbose_name='Adres e-mail (nieobowiązkowy)')
    text = models.TextField(verbose_name='Treść')
    www = models.URLField(verbose_name='Strona www autora (nieobowiązkowe)', blank=True)
    date = models.DateTimeField(verbose_name='Data dodania')
    removed = models.BooleanField(verbose_name='Usunięty')
    class Meta:
        verbose_name = u"Komentarz"
        verbose_name_plural = u"Komentarze"
        ordering = ['-date']
    def __unicode__(self):
	    return unicode(self.news)

class Photo(models.Model):
    item = models.ForeignKey(News)
    title = models.CharField(max_length=100, verbose_name = u"Tytuł" )
    image = ThumbnailImageField(upload_to='photos')
    caption = models.CharField(max_length=250, blank=True, verbose_name = u"Podpis")

    class Meta:
        ordering = ['title']
        verbose_name = u"Zdjęcie"
        verbose_name_plural = u"Zdjęcia"
    
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id': self.id})

class Film(models.Model):
    youtube_url_id = models.CharField(max_length=50, verbose_name = u"Identyfikator YouTube")
    title = models.CharField(max_length=250, verbose_name = u"Tytuł")
    description = models.TextField(verbose_name='Opis')
#    kazanie = models.BooleanField(verbose_name='Kazanie')
    date = models.DateTimeField(verbose_name='Data dodania')
    class Meta:
         verbose_name = u"Film"
         verbose_name_plural = u"Filmy"
         ordering = ['-date']

    def __unicode__(self):
        return self.title


class Kazanie(models.Model):
    youtube_url_id = models.CharField(max_length=50, verbose_name = u"Identyfikator YouTube")
    title = models.CharField(max_length=250, verbose_name = u"Tytuł")
    description = models.TextField(verbose_name='Opis')
    date = models.DateTimeField(verbose_name='Data dodania')
    class Meta:
         verbose_name = u"Kazanie"
         verbose_name_plural = u"Kazania"
         ordering = ['-date']

    def __unicode__(self):
        return self.title


class Katecheza(models.Model):
    youtube_url_id = models.CharField(max_length=50, verbose_name = u"Identyfikator YouTube")
    title = models.CharField(max_length=250, verbose_name = u"Tytuł")
    description = models.TextField(verbose_name='Opis')
    date = models.DateTimeField(verbose_name='Data dodania')
    class Meta:
         verbose_name = u"Katecheza"
         verbose_name_plural = u"Katechezy"
         ordering = ['-date']

    def __unicode__(self):
        return self.title

class File(models.Model):
    file = models.FileField(upload_to='content')
    date = models.DateTimeField(verbose_name='Data dodania')
    class Meta:
        verbose_name = u"Plik"
        verbose_name_plural = u"Pliki"
        ordering = ['-date']
    def __unicode__(self):
        return self.file.name

class Slide(models.Model):
    file = models.FileField(upload_to='content')
    date = models.DateTimeField(verbose_name='Data dodania')
    class Meta:
        verbose_name = u"Slajd"
        verbose_name_plural = u"Slajdy"
        ordering = ['-date']
    def __unicode__(self):
        return self.file.name


class Block(models.Model):
    title = models.CharField(max_length=100, verbose_name = u"Tytuł" )
    body = models.TextField(verbose_name=u'Treść')
    date = models.DateTimeField(verbose_name='Data dodania')
    published = models.BooleanField(verbose_name='Opublikowany')

    class Meta:
        verbose_name = u"Ramka"
        verbose_name_plural = u"Ramka"
        ordering = ['-date']
    def __unicode__(self):
        return self.title
