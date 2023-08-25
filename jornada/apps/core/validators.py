from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core import validators




def validate_file_size(value, MAX_SIZE=1024*1024, max_size_verbose="1MB"):
    filesize = value.size
    
    if filesize > MAX_SIZE:
        raise ValidationError(f"Você não pode fazer upload de arquivos maiores que {max_size_verbose}")
    else:
        return value



class CaracteresEspeciaisValidator(validators.RegexValidator):
    regex = r"^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÊÈÍÏÓÔÕÖÚÇ \(\)\']+$"
    flags = 0
    message = ("Digite um valor válido. Apenas caracteres alfabéticos.")


class SomenteNumeros(validators.RegexValidator):
    regex = r"^[0-9]*$"
    flags = 0
    message = ("Digite um valor válido. Apenas caracteres numéricos.")


def raise_validation_error(field:str, message:str) -> None:
    raise ValidationError({field:_(message)})

def to_decorator(validator, *vargs, **vkwargs):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            validator(self, *vargs, **vkwargs)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

valida = to_decorator

def require(obj, *fields, error_message = 'Esse campo é obrigatório'):
    for field in fields:
        if hasattr(obj, field) and getattr(obj,field) is None:
            raise_validation_error(field, error_message)

def block_changes(obj, *fields, error_message = 'Esse campo não pode ser alterado'):
    for field in fields:
        if field in obj.changes or field+"_id" in obj.changes:
            raise_validation_error(field, error_message)


def cidade_do_uf(obj):
    '''
        Checa se a Cidade pasasda pertence ao UF também passado.
    '''    
    if hasattr(obj, 'uf') and hasattr(obj, 'cidade'):
        if obj.uf and obj.cidade:
            if obj.uf != obj.cidade.uf:
                raise_validation_error('cidade', 'A Cidade selecionada não pertence ao UF selecionado')


