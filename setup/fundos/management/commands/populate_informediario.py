# your_app/management/commands/populate_table_from_csv.py
import os
import requests
import zipfile
import csv
import sys
from django.core.management.base import BaseCommand
from fundos.models import InformeDiario
from urllib.parse import urlparse
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Baixa, extrai e popula a tabela InformeDiario com dados do CSV e mostra a memória usada.'

    def handle(self, *args, **kwargs):
        base_url = 'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{}.zip'
        start_date = datetime.strptime('202405', '%Y%m')
        end_date = datetime.strptime('202101', '%Y%m')
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        downloads_dir = os.path.join(current_dir, "downloads")
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        while start_date >= end_date:
            url = base_url.format(start_date.strftime('%Y%m'))
            last_part = url.split("/")[-1]

            self.stdout.write(f'Iniciando com o arquivo {last_part}')
            local_zip_path = os.path.join(downloads_dir, last_part)

            # Baixar o arquivo ZIP
            self.stdout.write('Baixando o arquivo ZIP...')
            response = requests.get(url)
            if response.status_code == 200:
                with open(local_zip_path, 'wb') as file:
                    file.write(response.content)
                self.stdout.write('Arquivo ZIP baixado com sucesso.')
            else:
                self.stderr.write(f'Falha ao baixar o arquivo ZIP de {url}. Pulando para o próximo.')
                start_date = self.decrement_month(start_date)
                continue

            # Verificar a integridade do arquivo ZIP
            self.stdout.write('Verificando a integridade do arquivo ZIP...')
            if not zipfile.is_zipfile(local_zip_path):
                self.stderr.write(f'O arquivo baixado {last_part} não é um arquivo ZIP válido. Pulando para o próximo.')
                start_date = self.decrement_month(start_date)
                continue

            # Extrair o arquivo CSV
            self.stdout.write('Extraindo o arquivo CSV...')
            with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
                zip_ref.extractall(downloads_dir)

            extracted_files = zip_ref.namelist()
            if not extracted_files:
                self.stderr.write(f'Nenhum arquivo encontrado no ZIP {last_part}. Pulando para o próximo.')
                start_date = self.decrement_month(start_date)
                continue

            csv_filename = os.path.join(downloads_dir, extracted_files[0])
            if not os.path.exists(csv_filename):
                self.stderr.write(f'Arquivo CSV não encontrado no arquivo ZIP {last_part}. Pulando para o próximo.')
                start_date = self.decrement_month(start_date)
                continue

            # Inserir dados do CSV na tabela
            self.stdout.write('Populando a tabela com dados do CSV...')
            try:
                with open(csv_filename, newline='', encoding='latin-1') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';')
                    fieldnames = reader.fieldnames
                    batch_size = 1000
                    total_memory = 0
                    objs_to_create = []
                    objs_existing = set(InformeDiario.objects.all().values_list('CNPJ_FUNDO', 'DT_COMPTC'))
                    for row in reader:
                        obj_data = {field: row[field] for field in fieldnames}
                        obj = InformeDiario(**obj_data)
                        obj_tuple = (obj.CNPJ_FUNDO, obj.DT_COMPTC)
                        if obj_tuple not in objs_existing:
                            objs_to_create.append(obj)
                            objs_existing.add(obj_tuple)
                            total_memory += sys.getsizeof(obj)
                        if len(objs_to_create) >= batch_size:
                            InformeDiario.objects.bulk_create(objs_to_create, batch_size=batch_size)
                            objs_to_create.clear()
                    if objs_to_create:
                        InformeDiario.objects.bulk_create(objs_to_create, batch_size=batch_size)
                        total_memory += sum(sys.getsizeof(obj) for obj in objs_to_create)
                    
                    total_memory_kb = total_memory / 1024
                    self.stdout.write(self.style.SUCCESS(f'Foram inseridos {total_memory_kb:.2f} KB na tabela'))
                    self.stdout.write(self.style.SUCCESS(f'Arquivo {last_part} foi populado com sucesso.'))
            except Exception as e:
                self.stderr.write(f'Erro ao inserir dados do arquivo {last_part}: {e}')
            
            start_date = self.decrement_month(start_date)

    def decrement_month(self, date):
        year = date.year
        month = date.month
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        return datetime(year, month, 1)
