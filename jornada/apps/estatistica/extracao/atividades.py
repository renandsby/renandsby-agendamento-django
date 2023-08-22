from atividades.models import HistoricoAtividade
from django.db.models import Count
from datetime import datetime


@staticmethod
def get_atividades():
    historico_atividades = HistoricoAtividade.objects.filter(
        realizada=True,
        # data_ida__year=datetime.now().strftime("%Y"),
        # data_ida__month=datetime.now().strftime("%m")
    )
    atividades = historico_atividades.values("atividade__descricao").annotate(
        Count("atividade__descricao")
    )
    return atividades
