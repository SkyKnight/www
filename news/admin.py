# -*- coding: utf-8 -*-
from django.contrib import admin

from news.models import *

#class CategoryAdmin(admin.ModelAdmin):
#	list_display = ('name','icon')
#	prepopulated_fields = {'slug': ('name',)}

def make_published(modeladmin, request, queryset):
    if request.user.is_superuser:
        queryset.update(published=True)
make_published.short_description = u"Opublikuj wybrane artykuły"

def make_unpublished(modeladmin, request, queryset):
    if request.user.is_superuser:
        queryset.update(published=False)
make_unpublished.short_description = u"Wstrzymaj publikację wybranych artykułów"

def make_zatw(modeladmin, request, queryset):
    if request.user.is_superuser:
        queryset.update(published=True)
        queryset.update(status='Z')
make_zatw.short_description = u"Zatwierdź wybrane artykuły"

def make_unzatw(modeladmin, request, queryset):
    if request.user.is_superuser:
        queryset.update(published=False)
        queryset.update(status='B')
make_unzatw.short_description = u"Usuń zatwierdzenie wybranych artykułów"

def make_archive(modeladmin, request, queryset):
    if request.user.is_superuser:
        queryset.update(published=False)
        queryset.update(status='A')
make_archive.short_description = u"Archiwizuj zaznaczone"


#class NewsAdmin(admin.ModelAdmin):
#    exclude = ('owner',)
#    list_display = ('title','date','owner', 'published')
#    prepopulated_fields = {'slug': ('title',)}
#    actions = [make_published, make_unpublished]
#
#    def save_model(self, request, obj, form, change):
#        if not change:
#            obj.owner = request.user
#        obj.save()


class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'news','text', 'date', 'id')
	list_filter = ('date',)

class PhotoInline(admin.StackedInline):
    model = Photo

class NewsAdmin(admin.ModelAdmin):
    exclude = ('owner', 'published')
    inlines = [PhotoInline]
    list_display = ('title','date','status','published','owner','newslet')
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_zatw, make_unzatw, make_archive]
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(NewsAdmin, self).has_change_permission(request, obj)
        if request.user.pk in (1,3):
            return True
        if not has_class_permission:
            return False
#        if obj is not None and not request.user.is_superuser and request.user.id != obj.owner.id:
#        if obj is not None and request.user is not in (1,3) #and request.user.id != obj.owner.id: 
#            return False
        if obj is not None and obj.status=='Z':
            return False
        return True

#    def queryset(self, request):
#        if request.user.is_superuser:
#            return News.objects.all()
#        return News.objects.filter(owner=request.user)


class FilmAdmin(admin.ModelAdmin):
    list_display = ('title','date')
    list_filter = ('title',)

class KazanieAdmin(admin.ModelAdmin):
    list_display = ('title','date')
    list_filter = ('title',)

class KatechezaAdmin(admin.ModelAdmin):
    list_display = ('title','date')
    list_filter = ('title',)


class NewsletAdmin(admin.ModelAdmin):
    list_display = ('date','sent_date','unsent','report')
    list_filter = ('date',)


admin.site.register(Comment, CommentAdmin)
#admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Photo)
admin.site.register(Film, FilmAdmin)
admin.site.register(Kazanie, KazanieAdmin)
admin.site.register(Katecheza, KatechezaAdmin)
admin.site.register(Profile)
admin.site.register(Region)
admin.site.register(File)
admin.site.register(Newslet, NewsletAdmin)
admin.site.register(Block)
admin.site.register(Slide)
