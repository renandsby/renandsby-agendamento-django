from django.core.exceptions import ValidationError
from datetime import datetime

def logica_agendamento(obj):
    ...
    # if obj.s is None and obj.usuarios_relacionados is not None:
    #     obj.redeEmpresas = obj.modulo.redeEmpresas
    
    # if obj.adding:
    #     if (obj.data_hora is not None and obj.data_hora < datetime.now().timestamp()):
    #         raise ValidationError({'data_hora': 'Não é possível criar ocorrência com data anterior a data de hoje'})