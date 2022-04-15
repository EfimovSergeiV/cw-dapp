# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/m/m90099ra/m90099ra.beget.tech/main')
sys.path.insert(1, '/home/m/m90099ra/.local/bin/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
