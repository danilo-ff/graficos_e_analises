from django.urls import path
from .views import *

app_name = 'fundos'

urlpatterns = [
    path('index', index, name='index'),
    path('resultado', resultado, name='resultado'),
    path('fundo/<int:fundo_id>', grafico_fundo, name='grafico_fundo'),
    path('acao/<int:acao_id>', grafico_acao, name='grafico_acao'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('logout/', logout, name='logout'),
]