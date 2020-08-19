from django.contrib import admin
from newsletter.models import *

#class SubscriberAdmin(admin.ModelAdmin):
#    pass
admin.site.register(Body)
admin.site.register(Subscriber)
admin.site.register(Probne)
