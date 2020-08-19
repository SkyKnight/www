# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from tresc.models import *

class PhotoInline(admin.StackedInline):
    model = Photo


class StronaAdmin(admin.ModelAdmin):
    search_fields = ('tresc', 'tytul')
    inlines = [PhotoInline]
    list_display = ('tytul', 'slug')
    prepopulated_fields = {'slug' : ('tytul',)}

class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')    

admin.site.register(Strona, StronaAdmin)
admin.site.register(Link, LinkAdmin)
