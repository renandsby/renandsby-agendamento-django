from datetime import date

from adolescentes.models import Adolescente
from dominios.models import (Bairro, Genero, TipoEntradaUnidade,
                             SituacaoEscolar, TipoAtividade, TipoUnidade)
from unidades.models import EntradaAdolescente, Unidade


def get_adolescentes_lotados_ids():
    ids_adols = EntradaAdolescente.objects.filter(lotado=True).values_list(
        "adolescente__id", flat=True
    )
    return ids_adols


def get_adolescentes_lotados():
    adols = EntradaAdolescente.objects.filter(lotado=True)
    return adols


class Utils:
    @staticmethod
    def get_adolescentes_lotados():
        try:
            adolescentes = Adolescente.objects.all()
            adolescentes = [a for a in adolescentes if a.possui_entrada_ativa == True]
            return adolescentes
        except:
            pass

    @staticmethod
    def get_tipos_unidades():
        try:
            qs_tipo_unidades = TipoUnidade.objects.all()
            tipos_unidades = [
                {"id": u.id, "descricao": u.descricao} for u in qs_tipo_unidades
            ]
            return tipos_unidades
        except:
            pass

    @staticmethod
    def get_unidades():
        try:
            qs_unidades = Unidade.objects.all()
            unidades = [
                {"id": u.id, "sigla": u.sigla, "tipo_unidade_id": u.tipo_unidade_id}
                for u in qs_unidades
            ]
            return unidades
        except:
            pass

    @staticmethod
    def get_ras():
        try:
            qs_ras = Bairro.objects.all()
            ras = [{"id": ra.id, "nome": ra.nome} for ra in qs_ras]
            return ras
        except:
            pass

    @staticmethod
    def get_situacao_escolar():
        try:
            situacao_escolar = SituacaoEscolar.objects.all()
            situacoes = [
                {"id": s.id, "descricao": s.descricao} for s in situacao_escolar
            ]
            return situacoes
        except:
            pass

    @staticmethod
    def total_por_unidade():
        try:
            tipos_unidades = Utils.get_tipos_unidades()
            adolescentes = Utils.get_adolescentes_lotados()
            unidades = Utils.get_unidades()
            if tipos_unidades and adolescentes and unidades:
                total = []
                unidades_sigla = []
                tipo_unidade_descricao = []
                for unidade in unidades:
                    total.append(
                        len(
                            [
                                a
                                for a in adolescentes
                                if a.unidade_atual.id == unidade["id"]
                            ]
                        )
                    )
                    unidades_sigla.append(unidade["sigla"])
                    tipo_unidade_descricao.append(
                        [
                            tipo["descricao"]
                            for tipo in tipos_unidades
                            if unidade["tipo_unidade_id"] == tipo["id"]
                        ][0]
                    )
                return {
                    "total": total,
                    "unidades_sigla": unidades_sigla,
                    "tipo_unidade_descricao": tipo_unidade_descricao,
                }
        except:
            pass

    @staticmethod
    def get_idade(born):
        today = date.today()
        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )

    @staticmethod
    def total_por_idade():
        try:
            adolescentes = Utils.get_adolescentes_lotados()
            unidades = Utils.get_unidades()
            idades = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            idade_total = []
            unidades_sigla = []
            idade_label = []

            for idade in idades:
                for unidade in unidades:
                    idade_total.append(
                        len(
                            [
                                a
                                for a in adolescentes
                                if a.unidade_atual.id == unidade["id"]
                                and Utils.get_idade(a.data_nascimento) == idade
                            ]
                        )
                    )
                    unidades_sigla.append(unidade["sigla"])
                    idade_label.append(idade)

            return {
                "total": idade_total,
                "unidades_sigla": unidades_sigla,
                "idade_label": idade_label,
            }

        except:
            pass

    @staticmethod
    def total_tipo_entrada():
        entrada = []
        total = []

        try:
            adolescentes = Adolescente.objects.all()
            motivos = TipoEntradaUnidade.objects.all()
            for motivo in motivos:
                entrada.append(motivo.descricao)
                total.append(
                    len(
                        [
                            adolescente.entrada_em_unidade_atual.tipo_entrada.descricao
                            for adolescente in adolescentes
                            if adolescente.entrada_em_unidade_atual
                            and adolescente.entrada_em_unidade_atual.tipo_entrada.id
                            == motivo.id
                        ]
                    )
                )

        except:
            pass

        return {"entrada": entrada, "total": total}

    @staticmethod
    def total_tipo_atividade():
        atividade = []
        qtd_atividades = []
        total = []

        try:
            adolescentes = Adolescente.objects.all()
            for adolescente in adolescentes:
                qtd_atividades.append(
                    list(
                        adolescente.historico_atividades.filter(
                            realizada=True
                        ).values_list("atividade__tipo_atividade__id", flat=True)
                    )
                )
            tipos = TipoAtividade.objects.all()
            for tipo in tipos:
                atividade.append(tipo.descricao)
                total.append(
                    len([t for qtd in qtd_atividades for t in qtd if t == tipo.id])
                )

        except:
            pass

        return {"atividade": atividade, "total": total}

    @staticmethod
    def situacao_escolar_por_unidade():
        labels = []
        parents = []
        values = []
        try:
            adolescentes = Utils.get_adolescentes_lotados()
            unidades = Utils.get_unidades()
            situacoes = Utils.get_situacao_escolar()
            if unidades and situacoes and adolescentes:
                for unidade in unidades:

                    for situacao in situacoes:
                        labels.append(situacao["descricao"].replace(" ", "<br>", 2))
                        parents.append(unidade["sigla"])
                        values.append(
                            len(
                                [
                                    a
                                    for a in adolescentes
                                    if a.atendimento_educacao_atual
                                    and a.unidade_atual.id == unidade["id"]
                                    and a.atendimento_educacao_atual.situacao_escolar.id
                                    == situacao["id"]
                                ]
                            )
                        )

        except:
            pass

        return {
            "character": labels,
            "parent": parents,
            "value": values,
        }

    @staticmethod
    def situacao_escolar_por_ra():
        ras_label = []
        situacao_label = []
        total = []
        total_ra = []
        labels_ra = []
        total_sum = []
        try:
            adolescentes = Utils.get_adolescentes_lotados()
            ras = Utils.get_ras()
            situacoes = Utils.get_situacao_escolar()
            if ras and situacoes and adolescentes:
                for ra in ras:
                    total_ra.append(
                        len(
                            [
                                a
                                for a in adolescentes
                                if a.endereco_atual.bairro_id == ra["id"]
                            ]
                        )
                    )
                    labels_ra.append(ra["nome"])
                    for situacao in situacoes:
                        situacao_label.append(
                            situacao["descricao"].replace(" ", "<br>", 2)
                        )
                        ras_label.append(ra["nome"])
                        total.append(
                            len(
                                [
                                    a
                                    for a in adolescentes
                                    if a.atendimento_educacao_atual
                                    and a.endereco_atual.bairro_id == ra["id"]
                                    and a.atendimento_educacao_atual.situacao_escolar.id
                                    == situacao["id"]
                                ]
                            )
                        )

                        total_sum.append(
                            len(
                                [
                                    a
                                    for a in adolescentes
                                    if a.atendimento_educacao_atual.situacao_escolar
                                    and a.endereco_atual.bairro_id == ra["id"]
                                ]
                            )
                        )

        except:
            pass

        return {
            "ra": ras_label,
            "situacao": situacao_label,
            "total": total,
            "total_ra": total_ra,
            "labels_ra": labels_ra,
            "total_sum": total_sum,
            #    "se_ra_idade": Utils.situacao_escolar_por_ra_idade(),
        }

    @staticmethod
    def situacao_escolar_por_ra_idade():
        labels = []
        parents = []
        values = []
        idades = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        labels_ras = []
        labels_situacoes = []
        labels_idades = []
        labels_total = []
        try:
            adolescentes = Utils.get_adolescentes_lotados()
            ras = Utils.get_ras()
            situacoes = Utils.get_situacao_escolar()
            if ras and situacoes and adolescentes:
                for ra in ras:
                    for situacao in situacoes:
                        labels.append(situacao["descricao"].replace(" ", "<br>", 2))
                        parents.append(ra["nome"])
                        values.append(
                            len(
                                [
                                    a
                                    for a in adolescentes
                                    if a.atendimento_educacao_atual
                                    and a.endereco_atual.bairro_id == ra["id"]
                                    and a.atendimento_educacao_atual.situacao_escolar.id
                                    == situacao["id"]
                                ]
                            )
                        )
                        for idade in idades:
                            labels.append(str(idade))
                            parents.append(
                                situacao["descricao"].replace(" ", "<br>", 2)
                            )
                            values.append(
                                len(
                                    [
                                        a
                                        for a in adolescentes
                                        if a.atendimento_educacao_atual
                                        and a.endereco_atual.bairro_id == ra["id"]
                                        and a.atendimento_educacao_atual.situacao_escolar.id
                                        == situacao["id"]
                                        and Utils.get_idade(a.data_nascimento) == idade
                                    ]
                                )
                            )
                            labels_ras.append(ra["nome"])
                            labels_situacoes.append(
                                situacao["descricao"].replace(" ", "<br>", 2)
                            )
                            labels_idades.append(idade)
                            labels_total.append(
                                len(
                                    [
                                        a
                                        for a in adolescentes
                                        if a.atendimento_educacao_atual
                                        and a.endereco_atual.bairro_id == ra["id"]
                                        and a.atendimento_educacao_atual.situacao_escolar.id
                                        == situacao["id"]
                                        and Utils.get_idade(a.data_nascimento) == idade
                                    ]
                                )
                            )

        except:
            pass

        return {
            "character": labels,
            "parent": parents,
            "value": values,
            "ras": labels_ras,
            "situacoes": labels_situacoes,
            "idades": labels_idades,
            "total": labels_total,
        }

    @staticmethod
    def total_por_genero():
        generos = []
        total = []
        try:
            adolescentes = Utils.get_adolescentes_lotados()
            qs_genero = Genero.objects.all()
            if adolescentes and qs_genero:
                for genero in qs_genero:
                    generos.append(genero.descricao)
                    total.append(
                        len(
                            [
                                a
                                for a in adolescentes
                                if a.genero_id and a.genero_id == genero.id
                            ]
                        )
                    )
        except:
            pass

        return {"genero": generos, "total": total}
