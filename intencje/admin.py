# -*- coding: utf-8 -*-

from django.contrib import admin

from intencje.models import *

def make_published(modeladmin, request, queryset):
    queryset.update(active=True)
make_published.short_description = u"Opublikuj wybrane dni"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(active=False)
make_unpublished.short_description = u"Wstrzymaj publikację wybranych dni"

class DayAdmin(admin.ModelAdmin):
    list_display = ('date','name','active')
    actions = [make_published, make_unpublished]

    def queryset(self, request):
        return Day.objects.all()



admin.site.register(Day, DayAdmin)
