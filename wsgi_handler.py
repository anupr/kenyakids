import sys
import os
projectpath=os.path.dirname(os.path.abspath(__file__)) + '/..'
sys.path.append(projectpath)
sys.path.append(projectpath+"/mvdp")
os.environ['DJANGO_SETTINGS_MODULE'] = 'mvdp.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
