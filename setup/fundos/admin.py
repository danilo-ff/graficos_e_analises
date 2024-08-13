from django.contrib import admin
from .models import InformeDiario, CadFi

class InformeDiarioAdmin(admin.ModelAdmin):
    list_display = ('TP_FUNDO','CNPJ_FUNDO','DT_COMPTC','VL_TOTAL','VL_QUOTA','VL_PATRIM_LIQ','CAPTC_DIA','RESG_DIA','NR_COTST')
    list_display_links = ('CNPJ_FUNDO',)


admin.site.register(InformeDiario, InformeDiarioAdmin)

class CadFIAdmin(admin.ModelAdmin):
    list_display = ('CNPJ_FUNDO', 'DENOM_SOCIAL')
    
admin.site.register(CadFi, CadFIAdmin)

