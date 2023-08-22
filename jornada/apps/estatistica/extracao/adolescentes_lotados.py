from unidades.models import EntradaAdolescente
from django.db.models import Count
from datetime import datetime


@staticmethod
def get_adolescentes_lotados():
    entradas = EntradaAdolescente.objects.filter(
        lotado=True,
        # data_entrada__year=datetime.now().strftime("%Y"),
        # data_entrada__month=datetime.now().strftime("%m")
    )
    tipo_unidade_adolescentes = entradas.values("unidade__tipo_unidade__descricao").annotate(
        Count("unidade__tipo_unidade__descricao")
    )
    return tipo_unidade_adolescentes
