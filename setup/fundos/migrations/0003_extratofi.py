# Generated by Django 5.0.6 on 2024-05-13 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundos', '0002_rename_seumodelo_fundos'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtratoFi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CNPJ_FUNDO', models.CharField(max_length=100)),
                ('DENOM_SOCIAL', models.CharField(max_length=100)),
                ('DT_COMPTC', models.CharField(max_length=100)),
                ('CONDOM', models.CharField(max_length=100)),
                ('NEGOC_MERC', models.CharField(max_length=100)),
                ('MERCADO', models.CharField(max_length=100)),
                ('TP_PRAZO', models.CharField(max_length=100)),
                ('PRAZO', models.CharField(max_length=100)),
                ('PUBLICO_ALVO', models.CharField(max_length=100)),
                ('REG_ANBIMA', models.CharField(max_length=100)),
                ('CLASSE_ANBIMA', models.CharField(max_length=100)),
                ('DISTRIB', models.CharField(max_length=100)),
                ('POLIT_INVEST', models.CharField(max_length=100)),
                ('APLIC_MAX_FUNDO_LIGADO', models.CharField(max_length=100)),
                ('RESULT_CART_INCORP_PL', models.CharField(max_length=100)),
                ('FUNDO_COTAS', models.CharField(max_length=100)),
                ('FUNDO_ESPELHO', models.CharField(max_length=100)),
                ('APLIC_MIN', models.CharField(max_length=100)),
                ('ATUALIZ_DIARIA_COTA', models.CharField(max_length=100)),
                ('PRAZO_ATUALIZ_COTA', models.CharField(max_length=100)),
                ('COTA_EMISSAO', models.CharField(max_length=100)),
                ('COTA_PL', models.CharField(max_length=100)),
                ('QT_DIA_CONVERSAO_COTA', models.CharField(max_length=100)),
                ('QT_DIA_PAGTO_COTA', models.CharField(max_length=100)),
                ('QT_DIA_RESGATE_COTAS', models.CharField(max_length=100)),
                ('QT_DIA_PAGTO_RESGATE', models.CharField(max_length=100)),
                ('TP_DIA_PAGTO_RESGATE', models.CharField(max_length=100)),
                ('TAXA_SAIDA_PAGTO_RESGATE', models.CharField(max_length=100)),
                ('TAXA_ADM', models.CharField(max_length=100)),
                ('TAXA_CUSTODIA_MAX', models.CharField(max_length=100)),
                ('EXISTE_TAXA_PERFM', models.CharField(max_length=100)),
                ('TAXA_PERFM', models.CharField(max_length=100)),
                ('PARAM_TAXA_PERFM', models.CharField(max_length=100)),
                ('PR_INDICE_REFER_TAXA_PERFM', models.CharField(max_length=100)),
                ('VL_CUPOM', models.CharField(max_length=100)),
                ('CALC_TAXA_PERFM', models.CharField(max_length=100)),
                ('INF_TAXA_PERFM', models.CharField(max_length=100)),
                ('EXISTE_TAXA_INGRESSO', models.CharField(max_length=100)),
                ('TAXA_INGRESSO_REAL', models.CharField(max_length=100)),
                ('TAXA_INGRESSO_PR', models.CharField(max_length=100)),
                ('EXISTE_TAXA_SAIDA', models.CharField(max_length=100)),
                ('TAXA_SAIDA_REAL', models.CharField(max_length=100)),
                ('TAXA_SAIDA_PR', models.CharField(max_length=100)),
                ('OPER_DERIV', models.CharField(max_length=100)),
                ('FINALIDADE_OPER_DERIV', models.CharField(max_length=100)),
                ('OPER_VL_SUPERIOR_PL', models.CharField(max_length=100)),
                ('FATOR_OPER_VL_SUPERIOR_PL', models.CharField(max_length=100)),
                ('CONTRAP_LIGADO', models.CharField(max_length=100)),
                ('INVEST_EXTERIOR', models.CharField(max_length=100)),
                ('APLIC_MAX_ATIVO_EXTERIOR', models.CharField(max_length=100)),
                ('ATIVO_CRED_PRIV', models.CharField(max_length=100)),
                ('APLIC_MAX_ATIVO_CRED_PRIV', models.CharField(max_length=100)),
                ('PR_INSTITUICAO_FINANC_MIN', models.CharField(max_length=100)),
                ('PR_INSTITUICAO_FINANC_MAX', models.CharField(max_length=100)),
                ('PR_CIA_MIN', models.CharField(max_length=100)),
                ('PR_CIA_MAX', models.CharField(max_length=100)),
                ('PR_FI_MIN', models.CharField(max_length=100)),
                ('PR_FI_MAX', models.CharField(max_length=100)),
                ('PR_UNIAO_MIN', models.CharField(max_length=100)),
                ('PR_UNIAO_MAX', models.CharField(max_length=100)),
                ('PR_ADMIN_GESTOR_MIN', models.CharField(max_length=100)),
                ('PR_ADMIN_GESTOR_MAX', models.CharField(max_length=100)),
                ('PR_EMISSOR_OUTRO_MIN', models.CharField(max_length=100)),
                ('PR_EMISSOR_OUTRO_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FI_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FI_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FIC_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FIC_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FI_QUALIF_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FI_QUALIF_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FIC_QUALIF_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FIC_QUALIF_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FI_PROF_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FI_PROF_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FIC_PROF_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FIC_PROF_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FII_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FII_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FIDC_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FIDC_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FICFIDC_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FICFIDC_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FIDC_NP_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FIDC_NP_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FICFIDC_NP_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FICFIDC_NP_MAX', models.CharField(max_length=100)),
                ('PR_COTA_ETF_MIN', models.CharField(max_length=100)),
                ('PR_COTA_ETF_MAX', models.CharField(max_length=100)),
                ('PR_CRI_MIN', models.CharField(max_length=100)),
                ('PR_CRI_MAX', models.CharField(max_length=100)),
                ('PR_TITPUB_MIN', models.CharField(max_length=100)),
                ('PR_TITPUB_MAX', models.CharField(max_length=100)),
                ('PR_OURO_MIN', models.CharField(max_length=100)),
                ('PR_OURO_MAX', models.CharField(max_length=100)),
                ('PR_TIT_INSTITUICAO_FINANC_BACEN_MIN', models.CharField(max_length=100)),
                ('PR_TIT_INSTITUICAO_FINANC_BACEN_MAX', models.CharField(max_length=100)),
                ('PR_VLMOB_MIN', models.CharField(max_length=100)),
                ('PR_VLMOB_MAX', models.CharField(max_length=100)),
                ('PR_ACAO_MIN', models.CharField(max_length=100)),
                ('PR_ACAO_MAX', models.CharField(max_length=100)),
                ('PR_DEBENTURE_MIN', models.CharField(max_length=100)),
                ('PR_DEBENTURE_MAX', models.CharField(max_length=100)),
                ('PR_NP_MIN', models.CharField(max_length=100)),
                ('PR_NP_MAX', models.CharField(max_length=100)),
                ('PR_COMPROM_MIN', models.CharField(max_length=100)),
                ('PR_COMPROM_MAX', models.CharField(max_length=100)),
                ('PR_DERIV_MIN', models.CharField(max_length=100)),
                ('PR_DERIV_MAX', models.CharField(max_length=100)),
                ('PR_ATIVO_OUTRO_MIN', models.CharField(max_length=100)),
                ('PR_ATIVO_OUTRO_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FMIEE_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FMIEE_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FIP_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FIP_MAX', models.CharField(max_length=100)),
                ('PR_COTA_FICFIP_MIN', models.CharField(max_length=100)),
                ('PR_COTA_FICFIP_MAX', models.CharField(max_length=100)),
            ],
        ),
    ]
