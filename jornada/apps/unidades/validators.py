from core.validators import raise_validation_error
from django.core.exceptions import ValidationError


def quarto_do_modulo(obj):
    if (obj.quarto is not None):
        if obj.modulo is None:
            if obj.unidade.modulos.count() == 1:
                obj.modulo = obj.unidade.modulos.first()
            else:
                raise raise_validation_error('quarto', f'Não pode preencher Quarto sem preencher Módulo.')    
        
        if obj.quarto.modulo != obj.modulo:
            raise raise_validation_error('quarto', f'O Quarto não pertence ao Módulo {obj.modulo}')

def modulo_da_unidade(obj):
    if (obj.modulo is not None and
        obj.unidade != obj.modulo.unidade):
        raise raise_validation_error('modulo', f'O Módulo não pertence à unidade {obj.unidade.sigla}')