import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Darshanam_AI_Python.settings')

application = get_wsgi_application()
