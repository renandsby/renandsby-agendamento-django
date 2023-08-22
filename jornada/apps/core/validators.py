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

def processo_do_adolescente(obj):
    '''
        Se o objeto tiver processo e adolescente, checa se o processo é do adolescente
    '''
    if hasattr(obj, 'processo') and hasattr(obj, 'adolescente'):
        if obj.processo is not None and obj.adolescente is not None:
            if obj.processo.adolescente != obj.adolescente:
                raise_validation_error('processo', f'O Processo selecionado não pertence a {obj.adolescente.nome}')


def cidade_do_uf(obj):
    '''
        Checa se a Cidade pasasda pertence ao UF também passado.
    '''    
    if hasattr(obj, 'uf') and hasattr(obj, 'cidade'):
        if obj.uf and obj.cidade:
            if obj.uf != obj.cidade.uf:
                raise_validation_error('cidade', 'A Cidade selecionada não pertence ao UF selecionado')



def preencheu(obj, campo):
    '''
        Checa se o campo foi preenchido
    '''
    if hasattr(obj, campo) and getattr(obj, campo) is None:
        raise ValidationError({f'{campo}':f'Favor informar {obj._meta.get_field(campo).verbose_name}'})



def adolescente_esta_lotado_em_alguma_unidade(obj):
    if not obj.adolescente.possui_entrada_ativa:
        raise ValidationError(
                f"O adolescente {obj.adolescente} não está em nenhuma unidade.")


def adolescente_nao_esta_lotado_em_nenhuma_unidade(obj):
    if obj.adding:
        if obj.adolescente is not None and obj.adolescente.possui_entrada_ativa:
            raise ValidationError(
                f"O adolescente {obj.adolescente} já está na unidade {obj.adolescente.unidade_atual}")


def adolescente_nao_tem_saida_pendente(obj):
    if obj.adolescente.tem_saida_pendente:
        raise ValidationError(
            f"O adolescente {obj.adolescente} tem Saída Pendente na unidade {obj.adolescente.unidade_saida_pendente}")


def adolescente_nao_tem_entrada_pendente(obj):
    if obj.adolescente.tem_entrada_pendente:
        raise ValidationError(
            f"O adolescente {obj.adolescente} tem Entrada Pendente na unidade {obj.adolescente.unidade_entrada_pendente}")
