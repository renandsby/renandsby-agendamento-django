from django.core.exceptions import ValidationError
from core.validators import processo_do_adolescente
from . validators import adolescente_ou_nome_adolescente

def logica_solicitacao(obj):
    from unidades.models import EntradaAdolescente

    processo_do_adolescente(obj)
    adolescente_ou_nome_adolescente(obj)
    
    if 'adolescente_id' in obj.changes or obj.adding:
        entradas_ativas_adolescente = EntradaAdolescente.objects.filter(adolescente=obj.adolescente).exclude(status=4)
        if entradas_ativas_adolescente.exists():
            entrada_ativa = entradas_ativas_adolescente.first()
            if entrada_ativa.processo is not None and 'processo_id' not in obj.changes:
                obj.processo = entrada_ativa.processo
    
    if obj.updating: 
        status_anterior = obj._previous['status']
        changes = obj.changes
        
        if obj.validada and status_anterior == obj.__class__.Status.AGUARDANDO_VALIDACAO:
            obj.status = obj.__class__.Status.VALIDADO    
        
        if not obj.validada and status_anterior == obj.__class__.Status.VALIDADO:
            obj.status = obj.__class__.Status.AGUARDANDO_VALIDACAO

    if obj.adding:
        if obj.validada:
            if obj.status is None or (obj.status is not None and obj.status == obj.__class__.Status.AGUARDANDO_VALIDACAO):
                obj.status = obj.__class__.Status.VALIDADO
    