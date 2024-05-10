from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# установить модуль настроек Django по умолчанию для приложения 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Использование строки здесь означает, что работник не должен сериализовать
# объект конфигурации для дочерних процессов.
# пространство имен 'CELERY' означает, что все связанные с celery конфигурационные ключи
# должны иметь префикс 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузка модулей задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()
