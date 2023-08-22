from django.core.exceptions import ValidationError


def adolescente_ou_nome_adolescente(obj):
    if not obj.adolescente and not obj.nome_adolescente:
        raise ValidationError({"nome_adolescente":"O nome do adolescente é obrigatório."})
