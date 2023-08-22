from django.core.exceptions import ValidationError
def logica_ocorrencia(obj):
    if obj.unidade is None and obj.modulo is not None:
        obj.unidade = obj.modulo.unidade
    
    if obj.adding:
        if obj.modulo is not None:
            if obj.modulo.ultimo_livro is not None:
                if (obj.data_hora is not None and obj.data_hora < obj.modulo.ultimo_livro.data_abertura):
                    raise ValidationError({'data_hora': 'Não é possível criar ocorrência com data anterior ao plantão atual'})