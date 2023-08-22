from unidades.models import EntradaAdolescente
from django.db.models import Count


@staticmethod
def get_adolescentes_por_unidade_internacao():
    internacao = EntradaAdolescente.objects.filter(lotado=True, unidade__tipo_unidade__id=1)
    internacao_unidades_total = internacao.values("unidade__sigla").annotate(
        Count("unidade__sigla")
    )
    return internacao_unidades_total
