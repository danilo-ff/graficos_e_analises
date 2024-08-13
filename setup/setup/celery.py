# myproject/celery.py

# setup/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

app = Celery('setup')

# Configurações do Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregar tarefas de todos os aplicativos Django configurados
app.autodiscover_tasks()

# Schedule para executar a tarefa diariamente à meia-noite
app.conf.beat_schedule = {
    'run-update-diario-every-day': {
        'task': 'fundos.tasks.run_update_diario',
        'schedule': crontab(hour=0, minute=0),
    },
}

if __name__ == '__main__':
    app.start()
