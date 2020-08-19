# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from odpowiedzi.models import *

#class Admin(admin.ModelAdmin):
#    search_fields = ('tresc', 'tytul')
#    inlines = [PhotoInline]
#    list_display = ('tytul', 'slug')
#    prepopulated_fields = {'slug' : ('tytul',)}

#class LinkAdmin(admin.ModelAdmin):
#    list_display = ('title', 'slug')    

admin.site.register(Pytanie)

