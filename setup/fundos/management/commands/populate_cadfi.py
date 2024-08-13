import os
import requests
import csv
import sys
from django.core.management.base import BaseCommand
from fundos.models import CadFi
from datetime import datetime

class Command(BaseCommand):
    help = 'Baixa, extrai e popula a tabela CadFi com dados do CSV e mostra a memória usada.'

    def handle(self, *args, **kwargs):
        csv_url = 'https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv'
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        downloads_dir = os.path.join(current_dir, "downloads")
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        local_csv_path = os.path.join(downloads_dir, 'cad_fi.csv')

        # Baixar o arquivo CSV
        self.stdout.write('Baixando o arquivo CSV...')
        response = requests.get(csv_url)
        if response.status_code == 200:
            with open(local_csv_path, 'wb') as file:
                file.write(response.content)
            self.stdout.write('Arquivo CSV baixado com sucesso.')
        else:
            self.stderr.write(f'Falha ao baixar o arquivo CSV de {csv_url}.')
            return

        # Function to convert date strings to YYYY-MM-DD format
        def parse_date(date_str):
            if date_str:
                try:
                    return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    return None
            return None

        # Increase the maximum field size limit
        csv.field_size_limit(10 * 1024 * 1024)  # 10MB

        # Inserir dados do CSV na tabela
        self.stdout.write('Populando a tabela com dados do CSV...')
        try:
            with open(local_csv_path, newline='', encoding='latin-1') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                batch_size = 1000
                total_memory = 0
                objs_to_create = []
                objs_existing = set(CadFi.objects.values_list('CNPJ_FUNDO', flat=True))
                
                for row in reader:
                    obj_data = {field: row[field] for field in reader.fieldnames}
                    
                    # Parse date fields
                    date_fields = [
                        'DT_REG', 'DT_CONST', 'DT_CANCEL', 'DT_INI_SIT',
                        'DT_INI_ATIV', 'DT_INI_EXERC', 'DT_FIM_EXERC',
                        'DT_INI_CLASSE', 'DT_PATRIM_LIQ'
                    ]
                    for field in date_fields:
                        obj_data[field] = parse_date(obj_data[field])
                    
                    obj = CadFi(**obj_data)
                    
                    if obj.CNPJ_FUNDO not in objs_existing:
                        objs_to_create.append(obj)
                        objs_existing.add(obj.CNPJ_FUNDO)
                        total_memory += sys.getsizeof(obj)
                    
                    if len(objs_to_create) >= batch_size:
                        CadFi.objects.bulk_create(objs_to_create, batch_size=batch_size)
                        objs_to_create.clear()
                
                if objs_to_create:
                    CadFi.objects.bulk_create(objs_to_create, batch_size=batch_size)
                    total_memory += sum(sys.getsizeof(obj) for obj in objs_to_create)
                
                total_memory_kb = total_memory / 1024
                self.stdout.write(self.style.SUCCESS(f'Foram inseridos {total_memory_kb:.2f} KB na tabela'))
                self.stdout.write(self.style.SUCCESS('Tabela CadFi populada com sucesso.'))
        
        except Exception as e:
            self.stderr.write(f'Erro ao inserir dados do arquivo CSV: {e}')
