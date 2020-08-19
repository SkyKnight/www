import os
import sys
sys.path.append('/home/michal/django')
sys.path.append('/home/michal/django/nspj_parafia')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nspj_parafia.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

