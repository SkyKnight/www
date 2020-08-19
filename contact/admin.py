# -*- coding: utf-8 -*-
from django.contrib import admin
from contact.models import *

class ContactAdmin(admin.ModelAdmin):
	list_display = ('name','email','theme','adresat','date')

admin.site.register(Contact, ContactAdmin)
admin.site.register(Odpowiedz)
admin.site.register(Adresat)

