from django.views import View
from django.shortcuts import render
from datetime import date, datetime
from adolescentes.models import Adolescente, Endereco
from unidades.models import EntradaAdolescente
from dominios.models import Bairro

from alteracoes_vinculo.models import Vinculacao
from unidades.models import Unidade, VagaUnidade
from estatistica.dash.geral.dashboard_total_situacao_escolar_por_ra import Dashboard
from estatistica.dash.adolescentes.adolescentes_lotados import dashboard_adolescentes_lotados
from estatistica.dash.educacao.situacao_escolar import dashboard_situacao_escolar


class DashboardEstatistica(View):
    def get_idade(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def get_estatistica_geral(self, *args, **kwargs):
        data = {}
        data = {"data_referencia": datetime.now().strftime("%d/%m/%Y %H:%M")}
        dashboard_situacao_escolar()

        # Total de Adolescentes lotados
        dashboard_adolescentes_lotados()
        internacao = EntradaAdolescente.objects.filter(
            lotado=True, unidade__tipo_unidade__id=1
        ).count()
        semiliberdade = EntradaAdolescente.objects.filter(
            lotado=True, unidade__tipo_unidade__id=2
        ).count()
        meio_aberto = EntradaAdolescente.objects.filter(
            lotado=True, unidade__tipo_unidade__id=3
        ).count()
        atendimento_inicial = EntradaAdolescente.objects.filter(
            lotado=True, unidade__tipo_unidade__id=5
        ).count()
        total_adolescentes = EntradaAdolescente.objects.filter(lotado=True).count()
        if internacao > 0 and total_adolescentes > 0:
            perc_internacao = round((internacao / total_adolescentes) * 100, 2)
        else:
            perc_internacao = 0
        if semiliberdade > 0 and total_adolescentes > 0:
            perc_semiliberdade = round((semiliberdade / total_adolescentes) * 100, 2)
        else:
            perc_semiliberdade = 0
        if meio_aberto > 0 and total_adolescentes > 0:
            perc_meio_aberto = round((meio_aberto / total_adolescentes) * 100, 2)
        else:
            perc_meio_aberto = 0
        if atendimento_inicial > 0 and total_adolescentes > 0:
            perc_atendimento_inicial = round((atendimento_inicial / total_adolescentes) * 100, 2)
        else:
            perc_atendimento_inicial = 0

        data.update(
            {
                'total_adolescentes': total_adolescentes,
                'internacao': internacao,
                'semiliberdade': semiliberdade,
                'meio_aberto': meio_aberto,
                'atendimento_inicial': atendimento_inicial,
            }
        )

        # Adolescentes por RA
        adolescentes = list(Adolescente.objects.all())
        qs_bairro = list(Bairro.objects.all())
        bairros = [g for g in qs_bairro]
        ra_labels = []
        ra_values = []
        for bairro in bairros:
            ra_labels.append(bairro.nome)
            ra_values.append(
                len(
                    [
                        adolescente
                        for adolescente in adolescentes
                        if adolescente.possui_entrada_ativa == True
                        and adolescente.endereco_atual.bairro_id == bairro.id
                    ]
                )
            )

        data.update({'ra_labels': ra_labels, 'ra_values': ra_values})

        # Total de Vagas na Internação
        qs_unidades_internacao = Unidade.objects.filter(tipo_unidade__descricao="Internação")
        unidades_id = [unidade.id for unidade in qs_unidades_internacao]
        qs_vagas_unidade = VagaUnidade.objects.all()
        total_vagas = []
        for id in unidades_id:
            total_vagas.append(
                [vagas.quantidade for vagas in qs_vagas_unidade if vagas.unidade_id == id]
            )
        somatorio_vagas = 0
        for i in range(1, len(total_vagas)):
            somatorio_vagas += sum(total_vagas[i - 1])

        capacidade_internacao = round((total_adolescentes / somatorio_vagas) * 100, 2)
        data.update({'capacidade_internacao': capacidade_internacao})

        return data

    def render_estatistica(self):
        return render(
            self.request,
            'estatistica/dashboard/dashboard_teste.html',
        )

    def get(self, request, *args, **kwargs):
        return self.render_estatistica()
