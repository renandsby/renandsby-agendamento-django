from django.core.exceptions import ValidationError

from core.validators import (
    require,
    block_changes,
    processo_do_adolescente,
)

from .validators import (
    quarto_do_modulo,
    modulo_da_unidade
)

def logica_entrada_em_unidade(obj):
    
    # Converte status em bool lotado
    if obj.status == 2 or obj.status == 3:
       obj.lotado = True
    else:
        obj.lotado = False

               
    # Se Lotado
    if obj.lotado:
        
        # Busca outras entradas em que o adolescente esteja lotado
        outras_entradas_lotado = obj.__class__.objects.filter(
            adolescente = obj.adolescente,
            lotado = True
        ).exclude(
            id=obj.id,
        )
        
        # Se existir, deve retornar erro.
        if outras_entradas_lotado.exists():
            _entrada = outras_entradas_lotado.first()
            raise ValidationError(
                f"O adolescente está na unidade {_entrada.unidade.sigla} [{_entrada.get_status_display()}]"
            )
        

        # Se lotado, deve prencher módulo e quarto caso a unidade os possua
        if obj.unidade.modulos.count() == 1:
            # se unidade tem só 1 módulo, já preenche com ele.
            obj.modulo = obj.unidade.modulos.first()
            
            # exige quarto
            if obj.modulo.quartos.exists():
                require(obj, 'quarto', error_message='Preencha o quarto')
        else:
            # Se a unidade tem varios modulos, exige quarto e modulo
            require(obj, 'modulo', 'quarto', error_message=f'Preencha módulo e quarto')
    
    # Se entrada pendente
    if obj.status == 1:
        # Busca outras entradas com entrada pendente ou entrada realizada
        outras_entradas = obj.__class__.objects.filter(
            adolescente = obj.adolescente,
            status__in = [1,2]
        ).exclude(
            id=obj.id,
        )

        # Se existir retorna erro
        if outras_entradas.exists():
            _entrada = outras_entradas.first()
            raise ValidationError(
                f"O adolescente está na unidade {_entrada.unidade.sigla} [{_entrada.get_status_display()}]"
            )
    
    # if obj.status == 2 or obj.status == 3:
    #     require(obj, 'data_entrada', error_message='Preencha a data de entrada do adolescente')

    # campos bloqueados depois de lotado (usando previous pra garantir)
    if obj.updating and obj._previous['lotado'] == True:
        # bloqueia mudanças de adolescente e unidade
        block_changes(obj, 'adolescente', 'unidade') 


    # SEMPRE CHECA
    processo_do_adolescente(obj)
    quarto_do_modulo(obj)
    modulo_da_unidade(obj)

def nao_tem_outra_entrada_lotado(adolescente):
    from unidades.models import EntradaAdolescente
    # Busca outras entradas em que o adolescente esteja lotado
    outras_entradas_lotado = EntradaAdolescente.objects.filter(
        adolescente = adolescente,
        lotado = True
    )
        
    # Se existir, deve retornar erro.
    if outras_entradas_lotado.exists():
        _entrada = outras_entradas_lotado.first()
        raise ValidationError(
            f"O adolescente está na unidade {_entrada.unidade.sigla} [{_entrada.get_status_display()}]"
        )
