from django.db.models import Count
from dominios.models import Genero
from estatistica.utils import (get_adolescentes_lotados,
                               get_adolescentes_lotados_ids)


def get_adolescentes_por_genero():
    # adols = get_adolescentes_lotados()
    ids_adols = get_adolescentes_lotados_ids()
    generos = (
        Genero.objects.filter(adolescente__id__in=ids_adols)
        .values("descricao")
        .annotate(Count("descricao"))
    )
    # generos = adols.values(
    #     "unidade__sigla",
    #     "adolescente__genero__descricao",
    # ).annotate(count_genero=Count("adolescente__genero__descricao"))
    return generos
