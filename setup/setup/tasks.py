# acoes/tasks.py

from celery import shared_task
import subprocess

@shared_task
def run_update_diario():
    result = subprocess.run(['python', 'C:\\Users\\DANILO\\OneDrive\\Documentos\\Aplicativos\\Python Scripts\\projetos_django\\fundos-django-1\\setup\\fundos\\management\\commands\\update_diario.py'], capture_output=True, text=True)
    return result.stdout
