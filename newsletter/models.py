# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(verbose_name='adres e-mail')
    accepted = models.BooleanField(default=False, verbose_name='Potwierdzony')
    subscription_date = models.DateTimeField(verbose_name='Data wysłania formularza')
    code = models.CharField(max_length=12, verbose_name='kod potwierdzający')

    def __unicode__(self):
        return self.email

class Body(models.Model):
    text = models.TextField(verbose_name='treść (czysty tekst)')
    text_html = models.TextField(verbose_name='treść (html)')
    sending_date = models.DateTimeField(verbose_name='data wysyłki')
    unsent = models.BooleanField(default=True, verbose_name='niewysłany')    
    def __unicode__(self):
        return str(self.sending_date)

#    class Meta:
#        ordering = ["-sending_date"]

class Probne(models.Model):
    email = models.EmailField(verbose_name='adres e-mail')
    def __unicode__(self):
        return self.email

