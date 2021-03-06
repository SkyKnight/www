# -*- coding: utf-8 -*- 
from django.db import models

# Create your models here.
    
class Day(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nazwa dnia liturgicznego', help_text='np. II "Niedziela Wielkanocna" lub "Wspomnienie Św. Jacka Wyznawcy"')
    date = models.DateField(verbose_name='data')
    intentions = models.TextField(verbose_name="intencje Mszy", blank=True)
    active = models.BooleanField(verbose_name="opublikowane na stronie")

    def get_str_date(self):
        acc_list = {
                  1:u"stycznia",
                  2:u"lutego",
                  3:u"marca",
                  4:u"kwietnia",
                  5:u"maja",
                  6:u"czerwca",
                  7:u"lipca",
                  8:u"sierpnia",
                  9:u"września",
                  10:u"października",
                  11:u"listopada",
                  12:u"grudnia"
                  }
        return str(self.date.day)+" "+acc_list[self.date.month]+" "+str(self.date.year)


    def __unicode__(self):
        return self.get_str_date() + " - " + self.name

    class Meta:
        verbose_name = u"Dzień liturgiczny"
        verbose_name_plural = u"Dni liturgiczne"
        ordering = ["-date"]
