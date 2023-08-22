from unidades.models import EntradaAdolescente
from solicitacoes.models import Solicitacao
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from datetime import datetime


@staticmethod
def get_month(month):
    match month:
        case 1:
            return "Janeiro"
        case 2:
            return "Fevereiro"
        case 3:
            return "Março"
        case 4:
            return "Abril"
        case 5:
            return "Maio"
        case 6:
            return "Junho"
        case 7:
            return "Julho"
        case 8:
            return "Agosto"
        case 9:
            return "Setembro"
        case 10:
            return "Outubro"
        case 11:
            return "Novembro"
        case 12:
            return "Dezembro"


@staticmethod
def get_solicitacoes():
    try:
        s = Solicitacao.objects.filter(data_solicitacao__year=datetime.now().year)
        solicitacoes = list(
            s.values("data_solicitacao", "acao_solicitada__descricao").annotate(
                Count("acao_solicitada__descricao"), mes=ExtractMonth("data_solicitacao")
            )
        )
        return solicitacoes
    except:
        pass
