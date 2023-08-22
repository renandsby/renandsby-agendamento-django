from unidades.models import EntradaAdolescente
from adolescentes.models import Endereco
from django.db.models import Count


def get_adolescentes_por_ra():
    ids_adolescentes_lotados = EntradaAdolescente.objects.filter(lotado=True).values_list("adolescente__id", flat=True)
    enderecos = Endereco.objects.filter(adolescente__id__in=ids_adolescentes_lotados, reside=True)
    return enderecos.values("bairro__nome").annotate(count=Count("bairro__nome"))
