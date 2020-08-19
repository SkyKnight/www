# -*- coding: utf-8 -*-

from intencje.models import *
from django.views.generic.list_detail import object_list


def index(request):
    days = Day.objects.filter(active=True).reverse()
    return  object_list(
        request,
        days,
        paginate_by = 7,
        template_name = 'intencje.html')



    
