from django.core.exceptions import ValidationError
def logica_ocorrencia(obj):
    if obj.unidade is None and obj.modulo is not None:
        obj.unidade = obj.modulo.unidade
    
    if obj.adding:
        if obj.modulo is not None:
            ...