# -*- coding:utf-8 -*-
from django.db import models
from django import forms 
from django.contrib.auth.models import User
#from captcha.fields import CaptchaField
# Create your models here.

class Adresat(models.Model):
    user = models.OneToOneField(User)
    opis = models.CharField(max_length=255, verbose_name=u"Opis sprawowanej funkcji")
    visible = models.BooleanField(blank=True)
    def __unicode__(self):
        return self.opis
        
    class Meta:
        verbose_name=u"Adresat"
        verbose_name_plural=u'Adresaci'

class Contact(models.Model):
    adresat = models.ForeignKey(Adresat, verbose_name=u"Do kogo?")
    name = models.CharField(max_length=255, verbose_name=u"Imię, Nazwisko Nadawcy")
    theme = models.CharField(max_length=255, verbose_name=u"Temat", blank=True)
    email = models.EmailField(verbose_name=u"Adres poczty elektronicznej Nadawcy")
    message = models.TextField(verbose_name=u"Treść")
    cc_myself = models.BooleanField(blank=True, verbose_name=u"Kopia listu na mój adres")
    accord = models.BooleanField(blank=True)
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
#    captcha = CaptchaField()
    def __unicode__(self):
        return self.name +', '+  self.email +', '+ self.theme
    
    class Meta:
        verbose_name=u"List"
        verbose_name_plural=u'Listy Parafian i Czytelników'
        
class Odpowiedz(models.Model):
    list = models.ForeignKey(Contact, blank=True)
    theme = models.CharField(max_length=255, verbose_name=u"Temat", blank=True)
    message = models.TextField(verbose_name=u"Treść odpowiedzi")
    date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'Odpowiedź: ' + self.list.name +', '+  self.list.email +', '+ self.list.theme
    
    class Meta:
        verbose_name=u"Odpowiedź"
        verbose_name_plural=u'Odpowiedzi na listy'
    
class OdpowiedzForm(forms.ModelForm):
    class Meta:
        model=Odpowiedz
        exclude=['list',]
