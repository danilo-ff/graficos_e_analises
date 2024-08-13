import locale
from datetime import date, timedelta, datetime
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.db.models import Avg
import numpy as np
import plotly.graph_objs as go
from .models import CadFi, InformeDiario, TickerPesquisa
import pandas as pd
import yfinance as yf
from django.utils import timezone

class FundoBuscado:
    def __init__(self, fundo_id):
        self.dados_cadastrais = get_object_or_404(CadFi, pk=fundo_id)
        self.amostra = InformeDiario.objects.filter(CNPJ_FUNDO=self.dados_cadastrais.CNPJ_FUNDO).order_by('DT_COMPTC')
        
        self.today = date.today()
        self.twelve_months_ago = self.today - timedelta(days=365)
        
        self.amostra_12_meses = self.amostra.filter(DT_COMPTC__gte=self.twelve_months_ago)

        self.latest_price = self.amostra_12_meses.last().VL_QUOTA if self.amostra_12_meses.exists() else None
        self.twelve_months_price = self._get_closest_price(self.amostra, self.twelve_months_ago)
        
        self.latest_informe = self.amostra_12_meses.last() if self.amostra_12_meses.exists() else None
        
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        
        self.latest_VL_PATRIM_LIQ = (
            locale.currency(self.latest_informe.VL_PATRIM_LIQ, grouping=True).replace("R$", "").strip()
            if self.latest_informe else "N/A"
        )
        self.latest_NR_COTST = (
            f"{int(self.latest_informe.NR_COTST):,}"
            if self.latest_informe else "N/A"
        )
        
        self.average_VL_PATRIM_LIQ = (
            locale.currency(
                self.amostra_12_meses.aggregate(avg_VL_PATRIM_LIQ=Avg('VL_PATRIM_LIQ'))['avg_VL_PATRIM_LIQ'] or 0,
                grouping=True
            ).replace("R$", "").strip()
        )

        self.grafico_json = self._generate_grafico_json(self.amostra, self.dados_cadastrais)
        self.last_12_months_return = self._calculate_return(self.twelve_months_price, self.latest_price)
        self.volatility_12_months = self._calculate_volatility(self.amostra_12_meses)
        self.sharpe_ratio_12_months = self._calculate_sharpe_ratio(self.amostra_12_meses)
        self.grafico_cotistas = self._generate_grafico_cotistas(self.amostra)
        self.grafico_drawdown = self._generate_grafico_drawdown(self.amostra)
        self.grafico_patrimonio = self._grafico_patrimonio(self.amostra)
        self.grafico_volatilidade = self._grafico_volatilidade(self.amostra)


    def _generate_grafico_json(self, amostra, dados_cadastrais):
        datas = [x.DT_COMPTC for x in amostra]
        precos = [round(float(y.VL_QUOTA), 2) for y in amostra]

        trace = go.Scatter(x=datas, y=precos, name=dados_cadastrais.DENOM_SOCIAL)
        layout = go.Layout(title=dados_cadastrais.DENOM_SOCIAL, xaxis=dict(title='Datas'), yaxis=dict(title='Preços'))
        grafico_1 = go.Figure(data=[trace], layout=layout)

        grafico_1_json = grafico_1.to_json()
        return grafico_1_json

    def _get_closest_price(self, queryset, target_date):
        try:
            return queryset.filter(DT_COMPTC__lte=target_date).order_by('-DT_COMPTC').first().VL_QUOTA
        except AttributeError:
            return None

    def _calculate_return(self, start_price, end_price):
        if start_price is None or end_price is None:
            return "N/A"
        retorno = ((end_price - start_price) / start_price) * 100
        return f"{Decimal(retorno):.2f}"

    def _calculate_volatility(self, amostra):
        if not amostra.exists():
            return "N/A"
        price_list = list(amostra.values_list('VL_QUOTA', flat=True))
        daily_returns = np.diff(price_list) / price_list[:-1]
        volatility = np.std(daily_returns) * np.sqrt(252)  # Annualized volatility
        return f"{volatility:.2%}"

    def _calculate_sharpe_ratio(self, amostra, risk_free_rate=0.05):
        if not amostra.exists():
            return "N/A"
        price_list = list(amostra.values_list('VL_QUOTA', flat=True))
        daily_returns = np.diff(price_list) / price_list[:-1]
        mean_daily_return = np.mean(daily_returns)
        volatility = np.std(daily_returns) * np.sqrt(252)
        sharpe_ratio = (mean_daily_return * 252 - risk_free_rate) / volatility
        return f"{Decimal(sharpe_ratio):.2f}"
    
    def _generate_grafico_cotistas(self, amostra):
        datas = [x.DT_COMPTC for x in amostra]
        precos = [y.NR_COTST for y in amostra]

        trace = go.Scatter(x=datas, y=precos, name= "Cotistas")
        layout = go.Layout(title="Cotistas", xaxis=dict(title='Datas'), yaxis=dict(title='Cotistas'))
        grafico = go.Figure(data=[trace], layout=layout)

        grafico_json = grafico.to_json()
        return grafico_json
    
    def _generate_grafico_drawdown(self, amostra):
        if not amostra.exists():
            return "N/A"
        data = {'date': [x.DT_COMPTC for x in amostra], 'price': [float(x.VL_QUOTA) for x in amostra]}
        df = pd.DataFrame(data)
        df['max_to_date'] = df['price'].cummax()
        df['drawdown'] = df['price'] / df['max_to_date'] - 1
        
        trace = go.Scatter(x=df['date'], y=df['drawdown'], name="Drawdown")
        layout = go.Layout(title="Drawdown Over Time", xaxis=dict(title='Datas'), yaxis=dict(title='Drawdown'))
        drawdown_figure = go.Figure(data=[trace], layout=layout)

        drawdown_json = drawdown_figure.to_json()
        return drawdown_json
    
    def _grafico_patrimonio(self, amostra):
        datas = [x.DT_COMPTC for x in amostra]
        precos = [y.VL_PATRIM_LIQ for y in amostra]

        trace = go.Scatter(x=datas, y=precos, name= "Patrimônio")
        layout = go.Layout(title="Patrimônio", xaxis=dict(title='Datas'), yaxis=dict(title='Patrimônio'))
        grafico = go.Figure(data=[trace], layout=layout)

        grafico_json = grafico.to_json()
        return grafico_json
        
    def _grafico_volatilidade(self, amostra, window=30):
        if not amostra.exists():
            return "N/A"
        data = {'date': [x.DT_COMPTC for x in amostra], 'price': [float(x.VL_QUOTA) for x in amostra]}
        df = pd.DataFrame(data)
        
        # Calcular retornos diários
        df['daily_return'] = df['price'].pct_change()
        
        # Calcular volatilidade com janela móvel
        df['rolling_volatility'] = df['daily_return'].rolling(window=window).std() * np.sqrt(252)
        
        trace = go.Scatter(x=df['date'], y=df['rolling_volatility'], name="Volatility")
        layout = go.Layout(title="Volatility Over Time", xaxis=dict(title='Datas'), yaxis=dict(title='Volatility'))
        volatility_figure = go.Figure(data=[trace], layout=layout)

        volatility_json = volatility_figure.to_json()
        return volatility_json

class AcaoBuscada():
    def __init__(self, acao_id):
        self.grafico_json = self._generate_grafico_acao(acao_id)
        self.acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        self.rentabilidade_12m = self._calc_rentabilidade_12m(acao_id)
        self.rentabilidade_inicio = self._calc_rentabilidade_inicio(acao_id)
        self.volatilidade_12m = self._calc_volatilidade_12m(acao_id)
        self.volatilidade_inicio = self._calc_volatilidade_inicio(acao_id)
        self.sharpe_12m = self._calc_sharpe_12m(acao_id)
        self.sharpe_inicio = self._calc_sharpe_inicio(acao_id)
        self.grafico_drawdown = self._generate_grafico_drawdown(acao_id)
        self.grafico_volatilidade = self._generate_grafico_volatilidade(acao_id)

    def _generate_grafico_acao(self, acao_id):
        acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        ticker = acao.TICKER+'.SA'
        
        # Baixa todos os dados disponíveis
        data = yf.download(ticker, progress=False)['Close']

        # Atribui os índices a x e os preços a y
        datas = data.index
        precos = data.values

        trace = go.Scatter(x=datas, y=precos, name=acao.DENOM_SOCIAL)
        layout = go.Layout(title=acao.DENOM_SOCIAL, xaxis=dict(title='Datas'), yaxis=dict(title='Preços'))
        figura = go.Figure(data=[trace], layout=layout)

        # Converte o gráfico Plotly para JSON
        grafico_json = figura.to_json()

        return grafico_json

    def _calc_rentabilidade_12m(self, acao_id):
        acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        ticker = acao.TICKER+'.SA'
        data = yf.download(ticker, progress=False)['Close']
        
        # Calcular rentabilidade nos últimos 12 meses
        inicio_12m = datetime.now() - timedelta(days=365)
        dados_12m = data.loc[data.index >= inicio_12m]
        rentabilidade_12m = round((dados_12m.iloc[-1] / dados_12m.iloc[0] - 1) * 100, 2)

        return rentabilidade_12m

    def _calc_rentabilidade_inicio(self, acao_id):
        acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        ticker = acao.TICKER+'.SA'
        data = yf.download(ticker, progress=False)['Close']
        
        # Calcular rentabilidade desde o início dos dados
        rentabilidade_inicio = round((data.iloc[-1] / data.iloc[0] - 1) * 100, 2)

        return rentabilidade_inicio

    def _calc_volatilidade_12m(self, acao_id):
        acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        ticker = acao.TICKER+'.SA'
        data = yf.download(ticker, progress=False)['Close']
        
        # Calcular volatilidade nos últimos 12 meses
        inicio_12m = datetime.now() - timedelta(days=365)
        dados_12m = data.loc[data.index >= inicio_12m]
        retornos_diarios = dados_12m.pct_change().dropna()
        volatilidade_12m = round(np.std(retornos_diarios.values) * np.sqrt(252), 2)

        return volatilidade_12m

    def _calc_volatilidade_inicio(self, acao_id):
        acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        ticker = acao.TICKER+'.SA'
        data = yf.download(ticker, progress=False)['Close']
        
        # Calcular volatilidade desde o início dos dados
        retornos_diarios = data.pct_change().dropna()
        volatilidade_inicio = round(np.std(retornos_diarios.values) * np.sqrt(252), 2)

        return volatilidade_inicio

    def _calc_sharpe_12m(self, acao_id):
        acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        ticker = acao.TICKER+'.SA'
        data = yf.download(ticker, progress=False)['Close']
        
        # Calcular índice de Sharpe nos últimos 12 meses
        inicio_12m = datetime.now() - timedelta(days=365)
        dados_12m = data.loc[data.index >= inicio_12m]
        retornos_diarios = dados_12m.pct_change().dropna()
        retorno_anualizado = np.mean(retornos_diarios) * 252
        volatilidade = np.std(retornos_diarios) * np.sqrt(252)
        sharpe_12m = round(retorno_anualizado / volatilidade if volatilidade != 0 else 0, 2)

        return sharpe_12m

    def _calc_sharpe_inicio(self, acao_id):
        acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        ticker = acao.TICKER+'.SA'
        data = yf.download(ticker, progress=False)['Close']
        
        # Calcular índice de Sharpe desde o início dos dados
        retornos_diarios = data.pct_change().dropna()
        retorno_anualizado = np.mean(retornos_diarios) * 252
        volatilidade = np.std(retornos_diarios) * np.sqrt(252)
        sharpe_inicio = round(retorno_anualizado / volatilidade if volatilidade != 0 else 0, 2)

        return sharpe_inicio

    def _generate_grafico_drawdown(self, acao_id):
        acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        ticker = acao.TICKER+'.SA'
        data = yf.download(ticker, progress=False)['Close']

        # Calcular o drawdown desde o início
        retorno_acumulado = (data / data.iloc[0]) - 1
        drawdown = (retorno_acumulado - retorno_acumulado.cummax()) * 100

        trace = go.Scatter(x=data.index, y=drawdown, name='Drawdown', mode='lines')
        layout = go.Layout(title='Drawdown desde o início', xaxis=dict(title='Datas'), yaxis=dict(title='Drawdown (%)'))
        figura = go.Figure(data=[trace], layout=layout)

        # Converte o gráfico Plotly para JSON
        grafico_json = figura.to_json()

        return grafico_json

    def _generate_grafico_volatilidade(self, acao_id):
        acao = get_object_or_404(TickerPesquisa, pk=acao_id)
        ticker = acao.TICKER+'.SA'
        data = yf.download(ticker, progress=False)['Close']

        # Calcular a volatilidade desde o início com média móvel de 30 dias
        retornos_diarios = data.pct_change().dropna()
        volatilidade = retornos_diarios.rolling(window=30).std() * np.sqrt(252)

        trace = go.Scatter(x=data.index, y=volatilidade, name='Volatilidade', mode='lines')
        layout = go.Layout(title='Volatilidade desde o início', xaxis=dict(title='Datas'), yaxis=dict(title='Volatilidade'))
        figura = go.Figure(data=[trace], layout=layout)

        # Converte o gráfico Plotly para JSON
        grafico_json = figura.to_json()

        return grafico_json