from django.core.exceptions import ValidationError

def logica_visita(obj):
    obj.em_visita = True if obj.data_entrada is not None and obj.data_saida is None else False
    
    outras_visitas = obj.__class__.objects.filter(
        adolescente = obj.adolescente,
        visitante = obj.visitante,
        em_visita = True
    ).exclude(
        id=obj.id,
    )
    
    if obj.em_visita and outras_visitas.exists():
        raise ValidationError({'visitante':' Já existe uma visita em curso com este visitante'})

    
    if obj.modulo is not None:
        if obj.modulo.ultimo_livro is not None:
            if (
                (obj.data_entrada is not None and obj.data_entrada < obj.modulo.ultimo_livro.data_abertura) or
                (obj.data_saida is not None and obj.data_saida < obj.modulo.ultimo_livro.data_abertura)
            ):
                raise ValidationError(f'Não é possível registrar uma visita com datas anteriores ao Livro atual')