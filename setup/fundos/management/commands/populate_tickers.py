import requests
import pandas as pd
from django.core.management.base import BaseCommand
from fundos.models import TickerPesquisa
from tempfile import NamedTemporaryFile

class Command(BaseCommand):
    help = 'Baixa o arquivo CSV usando um token, filtra os dados e insere no banco de dados'

    def handle(self, *args, **kwargs):
        # Parâmetros para a primeira requisição
        request_name_url = "https://arquivos.b3.com.br/api/download/requestname"
        params = {
            "fileName": "InstrumentsConsolidatedFile",
            "date": "2024-05-31",
            "recaptchaToken": ""  # Presumivelmente, você pode precisar de um token válido aqui.
        }

        # Fazer a primeira requisição para obter o token
        try:
            response = requests.get(request_name_url, params=params)
            response.raise_for_status()  # Verifique se a requisição foi bem-sucedida
            token = response.json().get("token")
            if not token:
                raise ValueError("Não foi possível obter o token.")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao obter o token: {e}'))
            return

        # URL para a segunda requisição usando o token
        download_url = f"https://arquivos.b3.com.br/api/download/?token={token}"

        # Fazer a segunda requisição para baixar o arquivo
        try:
            download_response = requests.get(download_url)
            download_response.raise_for_status()  # Verifique se a requisição foi bem-sucedida
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao baixar o arquivo CSV: {e}'))
            return

        with NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(download_response.content)
            tmp_file.flush()
            csv_path = tmp_file.name

        # Verificar se o arquivo não está vazio
        if download_response.content.strip() == b'':
            self.stdout.write(self.style.ERROR('O arquivo CSV está vazio.'))
            return

        # Mostrar as primeiras linhas do CSV para depuração
        try:
            with open(csv_path, 'r', encoding='latin1') as file:
                lines = [next(file) for _ in range(10)]
                self.stdout.write(self.style.SUCCESS('Primeiras linhas do arquivo CSV:'))
                for line in lines:
                    self.stdout.write(line.strip())
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo CSV: {e}'))
            return

        # Carregar o CSV em um DataFrame pandas começando da segunda linha
        try:
            df = pd.read_csv(csv_path, sep=';', encoding='latin1', skiprows=1, on_bad_lines='skip', low_memory=False)  # Ajuste a codificação e separador conforme necessário
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo CSV: {e}'))
            return

        # Verificar se o DataFrame está vazio
        if df.empty:
            self.stdout.write(self.style.ERROR('O DataFrame está vazio após a leitura do arquivo CSV.'))
            return

        # Mostrar as colunas do DataFrame para depuração
        self.stdout.write(self.style.SUCCESS(f'Colunas do DataFrame: {list(df.columns)}'))

        # Verificar se as colunas 'SgmtNm' e 'SctyCtgyNm' estão presentes
        if 'SgmtNm' not in df.columns or 'SctyCtgyNm' not in df.columns:
            self.stdout.write(self.style.ERROR('Colunas necessárias não encontradas no DataFrame.'))
            return

        # Filtrar os dados
        filtered_df = df[(df['SgmtNm'] == 'CASH')]

        # Selecionar as colunas necessárias
        filtered_df = filtered_df[['TckrSymb', 'CrpnNm', 'ISIN']]

        # Renomear as colunas para corresponder ao modelo
        filtered_df.columns = ['TICKER', 'DENOM_SOCIAL', 'ISIN']

        # Limpar a tabela antes de inserir novos dados (opcional)
        TickerPesquisa.objects.all().delete()

        # Inserir os dados no banco de dados
        tickers = [
            TickerPesquisa(TICKER=row['TICKER'], DENOM_SOCIAL=row['DENOM_SOCIAL'], ISIN = row['ISIN'])
            for index, row in filtered_df.iterrows()
        ]
        TickerPesquisa.objects.bulk_create(tickers)

        self.stdout.write(self.style.SUCCESS('Dados inseridos com sucesso.'))
