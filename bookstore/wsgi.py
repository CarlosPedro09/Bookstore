import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
# Se quiser rodar local, use DEBUG=1
os.environ.setdefault('DEBUG', '1')
# Para local, pode deixar SECRET_KEY hardcoded
os.environ.setdefault('SECRET_KEY', 'django-insecure-v#3td1r@zk2mt#hn5=e--u+dg2j++j^vj3)6cdtddj5l5mc+7-')

application = get_wsgi_application()
