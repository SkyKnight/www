# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink
import datetime
from fields import ThumbnailImageField
# Create your models here.

class Strona(models.Model):
    tytul = models.CharField(max_length=120, verbose_name="tytuł")
    tresc = models.TextField(verbose_name="treść")
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Odnośnik')
    zmodyfikowany = models.DateTimeField(verbose_name="data modyfikacji", editable = False)
#    menu = models.CharField(max_length=120, verbose_name="element menu")
#    indeks = models.PositiveSmallIntegerField(verbose_name="pozycja w menu")
    hidden = models.BooleanField(verbose_name="ukryty")

    class Meta:
        verbose_name_plural = "Strony" 
#        ordering = ['indeks']
    def __unicode__(self):
        return self.tytul
    def get_absolute_url(self):
        return '/static/' + self.slug + '/'
    def save(self):
        self.zmodyfikowany = datetime.datetime.now()
        super(Strona, self).save()

class Photo(models.Model):
    item = models.ForeignKey(Strona)
    title = models.CharField(max_length=100, verbose_name = u"Tytuł" )
    image = ThumbnailImageField(upload_to='photos_stat')
    caption = models.CharField(max_length=250, blank=True, verbose_name = u"Pod\
pis")

    class Meta:
        ordering = ['title']
        verbose_name = u"Zdjęcie"
        verbose_name_plural = u"Zdjęcia"

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id': self.id})


class Link(models.Model):
    slug = models.CharField(max_length=255, unique=True, verbose_name='Odnośnik')
    title = models.CharField(max_length=255, verbose_name="tytuł")
    description = models.TextField(verbose_name='opis')
    weight = models.IntegerField(verbose_name='kolejność')

    class Meta:
        verbose_name_plural = "Linki"
        ordering = ['weight']
    def __unicode__(self):
        return self.title

    
   
