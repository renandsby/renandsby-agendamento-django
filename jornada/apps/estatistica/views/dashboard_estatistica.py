from django.views import View
from django.shortcuts import render
from datetime import date, datetime
from adolescentes.models import Adolescente, Endereco
from unidades.models import EntradaAdolescente
from dominios.models import Bairro

from solicitacoes.models import Solicitacao
from alteracoes_vinculo.models import Vinculacao
from unidades.models import Unidade, VagaUnidade
from estatistica.dash.geral.dashboard_total_situacao_escolar_por_ra import Dashboard
from estatistica.dash.adolescentes.adolescentes_lotados import dashboard_adolescentes_lotados
from estatistica.dash.tjdft.solicitacoes import dashboard_solicitacoes
from estatistica.dash.educacao.situacao_escolar import dashboard_situacao_escolar


class DashboardEstatistica(View):
    def get_idade(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def get_estatistica_geral(self, *args, **kwargs):
        data = {}
        data = {"data_referencia": datetime.now().strftime("%d/%m/%Y %H:%M")}
        dashboard_solicitacoes()
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

        # TJDFT Solicitações
        try:
            tjdft_solicitacoes_vinculacao = Solicitacao.objects.filter(
                acao_solicitada_id=1,
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            tjdft_solicitacoes_desvinculacao = Solicitacao.objects.filter(
                acao_solicitada_id=2,
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            tjdft_solicitacoes_transferencia = Solicitacao.objects.filter(
                acao_solicitada_id=3,
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            tjdft_solicitacoes_total = Solicitacao.objects.filter(
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            if tjdft_solicitacoes_vinculacao > 0 and tjdft_solicitacoes_total > 0:
                perc_vinculacao = round(
                    (tjdft_solicitacoes_vinculacao / tjdft_solicitacoes_total) * 100, 2
                )
            else:
                perc_vinculacao = 0
            if tjdft_solicitacoes_desvinculacao > 0 and tjdft_solicitacoes_total > 0:
                perc_desvinculacao = round(
                    (tjdft_solicitacoes_desvinculacao / tjdft_solicitacoes_total) * 100, 2
                )
            else:
                perc_desvinculacao = 0
            if tjdft_solicitacoes_transferencia > 0 and tjdft_solicitacoes_total > 0:
                perc_transferencia = round(
                    (tjdft_solicitacoes_transferencia / tjdft_solicitacoes_total) * 100, 2
                )
            else:
                perc_transferencia = 0

            data.update(
                {
                    'tjdft_solicitacoes_total': tjdft_solicitacoes_total,
                    'tjdft_solicitacoes_vinculacao': perc_vinculacao,
                    'tjdft_solicitacoes_desvinculacao': perc_desvinculacao,
                    'tjdft_solicitacoes_transferencia': perc_transferencia,
                }
            )

        except:
            pass

        # TJDFT Solicitações Status
        try:
            tjdft_solicitacoes_aguardando_validacao = Solicitacao.objects.filter(
                status=1,
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            tjdft_solicitacoes_validado = Solicitacao.objects.filter(
                status=2,
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            tjdft_solicitacoes_em_processamento = Solicitacao.objects.filter(
                status=3,
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            tjdft_solicitacoes_realizado = Solicitacao.objects.filter(
                status=4,
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            tjdft_solicitacoes_negado = Solicitacao.objects.filter(
                status=5,
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            tjdft_solicitacoes_total = Solicitacao.objects.filter(
                data_solicitacao__year=datetime.now().strftime("%Y"),
                data_solicitacao__month=datetime.now().strftime("%m"),
            ).count()
            if tjdft_solicitacoes_aguardando_validacao > 0 and tjdft_solicitacoes_total > 0:
                perc_aguardando_validacao = round(
                    (tjdft_solicitacoes_aguardando_validacao / tjdft_solicitacoes_total) * 100, 2
                )
            else:
                perc_aguardando_validacao = 0
            if tjdft_solicitacoes_validado > 0 and tjdft_solicitacoes_total > 0:
                perc_validado = round(
                    (tjdft_solicitacoes_validado / tjdft_solicitacoes_total) * 100, 2
                )
            else:
                perc_validado = 0
            if tjdft_solicitacoes_em_processamento > 0 and tjdft_solicitacoes_total > 0:
                perc_em_processamento = round(
                    (tjdft_solicitacoes_em_processamento / tjdft_solicitacoes_total) * 100, 2
                )
            else:
                perc_em_processamento = 0
            if tjdft_solicitacoes_realizado > 0 and tjdft_solicitacoes_total > 0:
                perc_realizado = round(
                    (tjdft_solicitacoes_realizado / tjdft_solicitacoes_total) * 100, 2
                )
            else:
                perc_realizado = 0
            if tjdft_solicitacoes_negado > 0 and tjdft_solicitacoes_total > 0:
                perc_negado = round((tjdft_solicitacoes_negado / tjdft_solicitacoes_total) * 100, 2)
            else:
                perc_negado = 0
            data.update(
                {
                    'tjdft_solicitacoes_aguardando_validacao': perc_aguardando_validacao,
                    'tjdft_solicitacoes_validado': perc_validado,
                    'tjdft_solicitacoes_em_processamento': perc_em_processamento,
                    'tjdft_solicitacoes_realizado': perc_realizado,
                    'tjdft_solicitacoes_negado': perc_negado,
                }
            )
        except:
            pass

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
