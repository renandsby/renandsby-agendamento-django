from unidades.models import EntradaAdolescente
from django.db.models import Count
from datetime import datetime


@staticmethod
def get_adolescentes_motivo_entrada():
    entradas = EntradaAdolescente.objects.filter(
        lotado=True,
        # data_entrada__year=datetime.now().strftime("%Y"),
        # data_entrada__month=datetime.now().strftime("%m")
    )
    entradas_motivos = entradas.values("tipo_entrada__descricao").annotate(
        Count("tipo_entrada__descricao")
    )
    return entradas_motivos
