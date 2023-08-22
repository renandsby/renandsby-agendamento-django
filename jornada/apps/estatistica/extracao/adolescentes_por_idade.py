from unidades.models import EntradaAdolescente
from adolescentes.models import Endereco
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import ExtractYear
import timeit


@staticmethod
def get_adolescentes_por_idade():
    entradas = EntradaAdolescente.objects.filter(lotado=True)
    idades_por_unidade = entradas.values("unidade__sigla").annotate(idade=timezone.now().year - ExtractYear("adolescente__data_nascimento"))
    total_idades_por_unidade = idades_por_unidade.values("unidade__sigla","idade").annotate(Count("idade"))
    return total_idades_por_unidade
