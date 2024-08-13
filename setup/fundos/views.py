from django.shortcuts import render, redirect
from .models import CadFi, TickerPesquisa
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib import auth
from django.contrib import messages
from .utils import *

# Create your views here.
def index(request):
    return render(request, 'fundos/index.html')

def resultado(request):
    if request.method =="GET":
        ativo_buscado = request.GET.get('busca','')
        acoes = TickerPesquisa.objects.filter(Q(DENOM_SOCIAL__icontains=ativo_buscado) | Q(TICKER__icontains=ativo_buscado))
        fundos = CadFi.objects.filter(DENOM_SOCIAL__icontains = ativo_buscado).exclude(SIT='CANCELADA')
        return render(request, 'fundos/resultados.html', {'acoes': acoes, 'fundos':fundos})

def grafico_fundo(request, fundo_id):
    try:
        fundo = FundoBuscado(fundo_id)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'fundos/grafico.html', {'fundo': fundo})

def grafico_acao(request, acao_id):
    try:
        acao = AcaoBuscada(acao_id)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'fundos/grafico_acao.html', {'fundo': acao})

def logout(request):
        auth.logout(request)
        messages.success(request, "Logout efetuado com sucesso!")
        return redirect('usuarios:login')


@require_GET
def autocomplete(request):
    query = request.GET.get('term', '')
    ticker_results = list(TickerPesquisa.objects.filter(
        Q(DENOM_SOCIAL__icontains=query) | Q(TICKER__icontains=query)
    ).values('id', 'DENOM_SOCIAL', 'TICKER')[:10])
    
    cadfi_results = list(CadFi.objects.filter(
        Q(DENOM_SOCIAL__icontains=query) & ~Q(SIT='CANCELADA')
    ).values('id', 'DENOM_SOCIAL')[:10])
    
    results = []

    for result in ticker_results:
        results.append({
            'id': result['id'],
            'name': result['DENOM_SOCIAL'],
            'type': 'TickerPesquisa',
            'extra': result['TICKER']
        })
    
    for result in cadfi_results:
        results.append({
            'id': result['id'],
            'name': result['DENOM_SOCIAL'],
            'type': 'CadFi',
            'extra': ''
        })
    
    return JsonResponse(results, safe=False)