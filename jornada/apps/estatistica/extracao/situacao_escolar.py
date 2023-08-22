from unidades.models import EntradaAdolescente
from educacao.models import AtendimentoEducacao
from django.db.models import Count
from datetime import datetime


@staticmethod
def get_situacao_escolar():
    entradas = EntradaAdolescente.objects.filter(
        lotado=True,
        # data_entrada__year=datetime.now().strftime("%Y"),
        # data_entrada__month=datetime.now().strftime("%m")
    )
    lista_adolescentes_lotados = entradas.values("adolescente_id")
    atendimento_educacao = AtendimentoEducacao.objects.filter(
        adolescente_id__in=lista_adolescentes_lotados
    ).order_by("-data_atendimento")
    situacao_escolar = atendimento_educacao.values("situacao_escolar__descricao").annotate(
        Count("situacao_escolar__descricao")
    )
    return situacao_escolar
