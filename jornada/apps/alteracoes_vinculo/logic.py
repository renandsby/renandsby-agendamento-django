from django.core.exceptions import ValidationError

def logica_desvinculacao(desv):
    from unidades.models import EntradaAdolescente
    if 'adolescente_id' in desv.changes or desv.adding:
        entradas_ativas_adolescente = EntradaAdolescente.objects.filter(adolescente=desv.adolescente).exclude(status=4)
        if entradas_ativas_adolescente.exists():
            
            if entradas_ativas_adolescente.count() == 1:
                entrada_antiga = entradas_ativas_adolescente.first()
            else:
                entrada_antiga = entradas_ativas_adolescente.filter(lotado=True).first()
                
            desv.entrada_antiga = entrada_antiga
            desv.unidade_origem = entrada_antiga.unidade
            desv.status_original_entrada_antiga = entrada_antiga.status
            if entrada_antiga.processo is not None:
                desv.processo = entrada_antiga.processo
    
    
    if desv.entrada_antiga is not None:
        from alteracoes_vinculo.models import Transferencia, Vinculacao, Desvinculacao
        
        for cls in (Transferencia, Vinculacao, Desvinculacao):
            other = cls._default_manager.filter(entrada_antiga__id=desv.entrada_antiga.id)
           
            if desv.pk and desv.__class__ == cls:
               other = other.exclude(pk=desv.pk)
            
            if other.exists():
                raise ValidationError(f"Duplicidade! Já existe uma {cls.__name__} para {desv.entrada_antiga.adolescente.nome} em {desv.entrada_antiga.unidade.sigla} criada em {other.first().criado_em.strftime('%d/%m/%Y')}")
            
            
def logica_vinculacao(vinc):
    ...