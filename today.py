# -*- coding: utf-8 -*-
#!/usr/bin/python
# TEMPLATE_CONTEXT_PROCESSOR

from intencje.models import Day



def today(request):
    import datetime
    today = datetime.date.today()
    try:
        liturg_day = Day.objects.get(date=today)
    except:
        liturg_day = False 
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
    10:"października",
    11:"listopada",
    12:"grudnia"
    }

    rom_list = ['0','I','II','III','IV','V','VI','VII','VIII','IX','X',
    'XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX',
    'XXI','XXII','XXIII','XXIV','XXV','XXVI','XXVII','XXVIII','XXIX','XXX',
    'XXXI','XXXII','XXXIII','XXXIV','XXXV','XXXVI','XXXVII','XXXVIII','XXXIX'
    ]

    acc_month = acc_list[today.month]

    import re
    def remove_html_tags(data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)    
    
    def to_rom(data):
        d = int(re.findall('^\d+', data)[0])
        p = re.compile('^\d+\.')
        return p.sub(rom_list[d], data)

#    import urllib
#    sock = urllib.urlopen("http://sun.aei.polsl.pl/~ksim/tradycja/ordo.php")
#    htmlSource = sock.read()
#    lista = htmlSource.split('</tr>')
#    lista2=lista[1].split('</td>')
#    i = 0
#    for item in lista2:
#        lista2[i]=remove_html_tags(item)
#        i = i + 1
#    try:
#        name = to_rom(lista2[5])
#    except:
#        name = lista2[5]
#    clas = lista2[3]
#    color = lista2[2]
#    comm = lista2[6]
    return {'today':today, 'month1':acc_month, 'liturg_day':liturg_day}#, 'name':name, 'clas':clas, 'color':color, 'comm':comm}
