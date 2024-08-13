# your_app/management/commands/delete_all_data.py
from django.core.management.base import BaseCommand
from fundos.models import InformeDiario

class Command(BaseCommand):
    help = 'Apaga todos os dados da tabela InformeDiario'

    def handle(self, *args, **kwargs):
        # Apagar todos os dados da tabela
        InformeDiario.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Todos os dados da tabela InformeDiario foram apagados com sucesso.'))
