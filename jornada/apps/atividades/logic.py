from django.core.exceptions import ValidationError
from datetime import timedelta, datetime

def logica_historico_atividade(obj):
    
    obj.em_atividade = True if obj.data_ida is not None and obj.data_retorno is None and not obj.retorno_indeterminado else False
        
    obj.agendado = True if obj.data_prevista_ida is not None else False
    
    obj.realizada = True if obj.data_ida is not None and obj.data_retorno is not None or obj.retorno_indeterminado else False
        

    if (obj.data_ida is None and obj.data_prevista_ida is None):
        raise ValidationError(f'Favor informar Data de Ida OU Data Prevista de Ida.')
    
    if obj.data_ida and obj.data_retorno:
        if obj.data_retorno <= obj.data_ida:
            raise ValidationError({'data_retorno':f'Retorno deve ser posterior à ida'})
        
    if obj.modulo is not None:
        if obj.modulo.ultimo_livro is not None:
            if obj.adding:
                if ((obj.data_ida is not None and obj.data_ida < obj.modulo.ultimo_livro.data_abertura) or
                    (obj.data_retorno is not None and obj.data_retorno < obj.modulo.ultimo_livro.data_abertura)):
                    raise ValidationError(f'Não é possível enviar/retornar adolescentes com datas anteriores ao plantão atual')
                
            if obj.updating:
                changes = obj.changes
                if (
                    ('data_ida' in changes.keys() and isinstance(changes['data_ida']['from'], datetime) and changes['data_ida']['from'] < obj.modulo.ultimo_livro.data_abertura) or
                    ('data_ida' in changes.keys() and isinstance(changes['data_ida']['to'], datetime) and changes['data_ida']['to'] < obj.modulo.ultimo_livro.data_abertura)
                    ):
                    raise ValidationError({'data_ida':f'Não é possível alterar informações com datas anteriores ao plantão atual'})
                if (('data_retorno' in changes.keys() and isinstance(changes['data_retorno']['from'], datetime) and changes['data_retorno']['from'] < obj.modulo.ultimo_livro.data_abertura) or
                    ('data_retorno' in changes.keys() and isinstance(changes['data_retorno']['to'], datetime) and changes['data_retorno']['to'] < obj.modulo.ultimo_livro.data_abertura)):
                    raise ValidationError({'data_retorno':f'Não é possível alterar informações com datas anteriores ao plantão atual'})
                
            
    
    if obj.em_atividade:
        idas_sem_retorno = obj.__class__._default_manager.filter(
            adolescente = obj.adolescente, 
            atividade__unidade = obj.atividade.unidade,
            em_atividade = True,
        ).exclude(id=obj.id)
        
        if idas_sem_retorno.exists():
            for ida in idas_sem_retorno:
                ida.retorno_indeterminado = True
                ida.em_atividade = False
                obs_antiga = ida.observacoes if ida.observacoes is not None else ""
                if len(obs_antiga) > 0:
                    obs_antiga += "\n"
                ida.observacoes = obs_antiga + f"Adolescente foi diretamente para a atividade {obj.atividade.nome_curto}."
                ida.realizada = True
                ida.save()

            

    if obj.agendado and not obj.em_atividade:
        outros_agendamentos_proximos = obj.__class__._default_manager.filter(
            adolescente = obj.adolescente, 
            atividade__unidade = obj.atividade.unidade,
            agendado = True,
            data_prevista_ida__gt = obj.data_prevista_ida - timedelta(minutes=15),
            data_prevista_ida__lt = obj.data_prevista_ida + timedelta(minutes=15)
        ).exclude(id=obj.id)
        
        
        if outros_agendamentos_proximos.exists():    
            raise ValidationError(f'Existe outro agendamento paro mesmo dia/horário (diferença deve ser maior que 15min)')
