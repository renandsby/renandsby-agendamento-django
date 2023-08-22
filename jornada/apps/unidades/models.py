import datetime
from itertools import chain

from adolescentes.models import Adolescente
from core.models import BaseModel
from core.models.utils import generate_uuid4_filename
from core.utils import TIPOS_VAGA_NAO_VINCULANTES
from core.validators import validate_file_size
from django.db import models
from django.db.models.functions import Cast
from django.utils import timezone
from geoposition.fields import GeopositionField

from .logic import logica_entrada_em_unidade


class Unidade(BaseModel):
    nome = models.CharField(max_length=255, null=True)
    sigla = models.CharField(max_length=255, null=True, unique=True)
    tipo_unidade = models.ForeignKey(
        "dominios.TipoUnidade", on_delete=models.SET_NULL, null=True
    )
    cep = models.CharField("CEP", max_length=8, blank=True, null=True)
    logradouro = models.CharField("Logradouro", max_length=255, blank=True, null=True)
    complemento = models.CharField("Complemento", max_length=255, blank=True, null=True)
    numero = models.CharField("Número", max_length=50, blank=True, null=True)
    uf = models.ForeignKey(
        "dominios.Uf",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="UF",
    )
    cidade = models.ForeignKey(
        "dominios.Cidade",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name="Cidade",
    )
    bairro = models.ForeignKey(
        "dominios.Bairro",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name="Bairro",
    )
    localizacao = GeopositionField(null=True, blank=True)
    regulamento_infracoes = models.ForeignKey(
        "dominios.RegulamentoInfracoes", on_delete=models.SET_NULL, null=True, blank=False, related_name='unidades'
    )

    vagas = models.ManyToManyField(
        "dominios.TipoVagaUnidade", through="VagaUnidade", related_name="vagas"
    )

    @property
    def agentes(self):
        return self.servidores.filter(
            cargo__descricao__in=["TSOCIO - AGENTE SOCIAL", "AGENTE SOCIOEDUCATIVO"]
        )

    @property
    def especialistas(self):
        return self.servidores.filter(cargo__descricao__startswith="ESOCIO")

    @property
    def ids_adolescentes_lotados(self):
        return self.adolescentes_lotados_entradas.values_list(
            "adolescente__id", flat=True
        )

    @property
    def adolescentes_lotados(self):
        return Adolescente.objects.filter(id__in=self.ids_adolescentes_lotados)

    @property
    def adolescentes_lotados_entradas(self):
        return self.entradas_de_adolescentes.filter(lotado=True).all()

    @property
    def adolescentes_com_entrada_pendente(self):
        return self.entradas_de_adolescentes.filter(status=1)

    @property
    def adolescentes_com_saida_pendente(self):
        return self.entradas_de_adolescentes.filter(status=3)

    @property
    def tipos_de_vaga(self):
        return self.vagas.all()

    @property
    def vagas_ocupadas(self):
        qs = (
            self.adolescentes_lotados_entradas.filter(tipo_vaga__isnull=False)
            .values("tipo_vaga__descricao")
            .annotate(total=models.Count("tipo_vaga__descricao"))
        )
        ocupadas = {vaga["tipo_vaga__descricao"]: vaga["total"] for vaga in qs}
        sem_tipo_vaga = self.adolescentes_lotados_entradas.filter(
            tipo_vaga__isnull=True
        )
        if sem_tipo_vaga.count() > 0:
            ocupadas["Outros"] = sem_tipo_vaga.count()
        return ocupadas

    @property
    def vagas_disponiveis(self):
        ocupadas = self.vagas_ocupadas
        disponiveis = {}

        for vaga in self.vagas_unidade.all():
            tipo = vaga.tipo_vaga.descricao
            if tipo not in disponiveis:
                disponiveis[tipo] = vaga.quantidade
                if tipo in ocupadas:
                    disponiveis[tipo] -= ocupadas[tipo]

        return disponiveis

    @property
    def resumo_vagas(self):
        ocupadas = self.vagas_ocupadas
        disponiveis = self.vagas_disponiveis
        resumo = {}
        for vaga in self.vagas_unidade.all():
            tipo = vaga.tipo_vaga.descricao
            if tipo not in resumo:
                resumo[tipo] = {
                    "total": vaga.quantidade,
                    "ocupadas": 0,
                    "disponiveis": vaga.quantidade,
                }

            if tipo in ocupadas:
                resumo[tipo]["ocupadas"] = ocupadas[tipo]

            if tipo in disponiveis:
                resumo[tipo]["disponiveis"] = disponiveis[tipo]

        for tipo in ocupadas:
            if tipo not in resumo and tipo not in disponiveis:
                resumo[tipo] = {
                    "total": 0,
                    "ocupadas": ocupadas[tipo],
                    "disponiveis": 0,
                }

        return resumo

    @property
    def quantidade_total_adolescentes(self):
        return self.entradas_de_adolescentes.filter(lotado=True).count()
    
    @property
    def quantidade_adolescentes_presentes(self):
        return int(self.quantidade_total_adolescentes - self.quantidade_adolescentes_evadidos - self.quantidade_adolescentes_em_atividade_externa)
    
    @property
    def quantidade_adolescentes_evadidos(self):
        return self.entradas_de_adolescentes.filter(lotado=True, evadido=True).count()
    
    @property
    def quantidade_adolescentes_em_atividade_externa(self):
        return len([entrada.id for entrada in self.entradas_de_adolescentes.filter(lotado=True) if entrada.em_atividade_externa])
    
    
    def __str__(self):
        return f"{self.sigla}"

    class Meta:
        ordering = ["sigla"]
        permissions = (
            ("acessar_todas", "Pode acessar o sistema de todas unidades"),
            ("acessar_todas_semiliberdades", "Pode acessar o sistema de todas unidades de Semiliberdade"),
            ("acessar_todas_geamas", "Pode acessar o sistema de todas unidades de Meio Aberto"),
            ("acessar_todas_internacoes", "Pode acessar o sistema de todas unidades de Internação"),
            ("editar_unidades", "Pode editar informações de unidades"),
            ("incluir_unidades", "Pode criar novas unidades"),
        )


class VagaUnidade(models.Model):
    unidade = models.ForeignKey(
        Unidade, on_delete=models.CASCADE, related_name="vagas_unidade"
    )
    tipo_vaga = models.ForeignKey("dominios.TipoVagaUnidade", on_delete=models.PROTECT)
    quantidade = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.unidade} vagas de {self.tipo_vaga}"

    class Meta:
        unique_together = ("tipo_vaga", "unidade")
        verbose_name_plural = "Vagas na Unidade"
        permissions = (
            ("ver_vagas", "Pode ver vagas de unidades"),
            ("editar_vagas", "Pode editar vagas de unidades"),
            ("incluir_vagas", "Pode criar novas vagas em unidades"),
        )


class Modulo(BaseModel):
    unidade = models.ForeignKey(
        Unidade, on_delete=models.CASCADE, related_name="modulos"
    )
    descricao = models.CharField(max_length=30)

    class Meta:
        unique_together = ("descricao", "unidade")
        ordering = ["unidade", "descricao"]
    
    @property
    def numero_modulo(self):
        return f"Módulo {self.descricao}"

    def __str__(self):
        if self.unidade.modulos.count() == 1:
            return f"Módulo {self.unidade}"
        return f"{self.unidade} - Módulo {self.descricao}"


    @property
    def _ids_entradas_adol_em_atividade_externa(self):
        return [entrada.id for entrada in self.entradas_atuais if entrada.em_atividade_externa]

    @property
    def entradas_adol_em_atividade_externa(self):    
        return self.entradas_atuais.filter(id__in = self._ids_entradas_adol_em_atividade_externa)
    
    @property
    def entradas_adol_no_modulo(self):
        return self.entradas_atuais.exclude(id__in = self._ids_entradas_adol_em_atividade_externa)

    @property
    def entradas_atuais(self):
        return self.entradas_de_adolescentes.filter(lotado=True, evadido=False).all()

    @property
    def quantidade_adolescentes(self):
        return self.entradas_atuais.count()

    @property
    def ids_adolescentes_lotados(self):
        return self.entradas_atuais.values_list("adolescente__id", flat=True)

    @property
    def adolescentes(self):
        return Adolescente.objects.filter(id__in=self.ids_adolescentes_lotados)

    @property
    def historico_atividades_plantao_atual(self):
        from atividades.models import HistoricoAtividade
        qs =  HistoricoAtividade.objects.filter(
            atividade__unidade=self.unidade,
            modulo = self,
        )
        qs = qs.filter(models.Q(realizada=True) | models.Q(em_atividade=True))
        
        return qs
        
    class Meta:
        ordering = ["descricao"]
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique",
                fields=["unidade", "descricao"],
            ),
        ]
        


class Quarto(BaseModel):
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="quartos",
    )
    numero = models.PositiveSmallIntegerField(verbose_name="Número do Quarto")
    nome = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Nome do Quarto (Opcional)"
    )
    vagas = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        if self.modulo.unidade.modulos.count() == 1:
            return f"{self.modulo.unidade.sigla} Quarto {self.numero}{self.nome}"
        return f"{self.modulo.unidade.sigla} Modulo {self.modulo.descricao} Quarto {self.numero}{self.nome}"

    @property
    def _ids_entradas_adol_em_atividade_externa(self):
        return [entrada.id for entrada in self.entradas_atuais if entrada.em_atividade_externa]

    @property
    def entradas_adol_em_atividade_externa(self):    
        return self.entradas_atuais.filter(id__in = self._ids_entradas_adol_em_atividade_externa)
    
    @property
    def entradas_adol_no_quarto(self):
        return self.entradas_atuais.exclude(id__in = self._ids_entradas_adol_em_atividade_externa)
    
    @property
    def entradas_atuais(self):
        return self.entradas_de_adolescentes.filter(lotado=True, evadido=False).all()

    @property
    def quantidade_adolescentes(self):
        return self.entradas_atuais.count()

    @property
    def ids_adolescentes_lotados(self):
        return self.entradas_atuais.values_list("adolescente__id", flat=True)

    @property
    def adolescentes(self):
        return Adolescente.objects.filter(id__in=self.ids_adolescentes_lotados)

    def clean(self):
        return super().clean()

    class Meta:
        ordering = ["modulo__unidade", "modulo", "numero", "nome"]
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_com_nome",
                fields=["modulo", "numero", "nome"],
            ),
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_sem_nome",
                fields=["modulo", "numero"],
                condition=models.Q(nome=None),
            ),
        ]


class EntradaAdolescente(BaseModel):
    class Status(models.IntegerChoices):
        ENTRADA_PENDENTE = 1, "Entrada Pendente"
        ENTRADA_REALIZADA = 2, "Lotado"
        SAIDA_PENDENTE = 3, "Lotado com Saída Pendente"
        SAIDA_REALIZADA = 4, "Saída Realizada"

    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.ENTRADA_PENDENTE,
        verbose_name="Status de Lotação",
    )

    lotado = models.BooleanField(default=False)
    evadido = models.BooleanField(default=False, verbose_name="Evadido?")

    unidade = models.ForeignKey(
        Unidade, on_delete=models.CASCADE, related_name="entradas_de_adolescentes"
    )

    adolescente = models.ForeignKey(
        Adolescente, on_delete=models.CASCADE, related_name="entradas_em_unidades"
    )

    processo = models.ForeignKey(
        "processos.Processo",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="entradas_relacionadas",
    )

    agente_referencia = models.ManyToManyField(
        "servidores.Servidor",
        related_name="referencias_como_agente",
        blank=True,
        verbose_name="Agente Referência",
    )

    especialista_referencia = models.ManyToManyField(
        "servidores.Servidor",
        related_name="referencias_como_especialista",
        blank=True,
        verbose_name="Especialista Referência",
    )

    tipo_vaga = models.ForeignKey(
        "dominios.TipoVagaUnidade",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name="Tipo de Vaga Ocupada",
    )

    ########################################################################################
    # ENTRADA
    data_prevista_entrada = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data Prevista De Entrada",
    )
    data_entrada = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Entrada",
    )
    tipo_entrada = models.ForeignKey(
        "dominios.TipoEntradaUnidade",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Tipo De Entrada",
    )
    observacoes_entrada = models.TextField(null=True, blank=True)

    # SAÍDA
    data_prevista_saida = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data Prevista De Saída",
    )
    data_saida = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data De Saída",
    )
    tipo_saida = models.ForeignKey(
        "dominios.TipoSaidaUnidade",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Tipo De Saída",
    )
    observacoes_saida = models.TextField(null=True, blank=True)

    ########################################################################################
    quarto = models.ForeignKey(
        Quarto,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="entradas_de_adolescentes",
    )
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="entradas_de_adolescentes",
        verbose_name="Módulo",
    )

    protetiva = models.BooleanField(default=False, verbose_name="Medida Protetiva")
    ########################################################################################

    def __str__(self):
        if self.status == self.__class__.Status.ENTRADA_PENDENTE:
            return f"{self.adolescente.nome} em {self.unidade} [ENTRADA PENDENTE]"
        if self.status == self.__class__.Status.ENTRADA_REALIZADA:
            return f"{self.adolescente.nome} em {self.unidade} [ENTRADA REALIZADA]"
        if self.status == self.__class__.Status.SAIDA_PENDENTE:
            return f"{self.adolescente.nome} em {self.unidade} [SAÍDA PENDENTE]"
        
        return f"{self.adolescente.nome} em {self.unidade} até {self.data_saida} [SAÍDA REALIZADA]"

    class Meta:
        verbose_name = "Entrada de Adolescente em Unidade"
        verbose_name_plural = "Entradas de Adolescentes em Unidades"
        ordering = ["-id"]
        permissions = (
            ("ver_entradas", "Pode ver entradas de adolescentes em unidades"),

            ("ver_entradas_da_unidade", "Pode ver entradas de adolescentes na unidade em que está lotado."),
            ("ver_chegadas", "Pode ver chegadas previstas de adolescentes em unidades"),
            ("ver_saidas", "Pode ver saídas previstas de adolescentes em unidades"),
            
            ("editar_entradas", "Pode editar entradas de adolescentes"),
            ("editar_entradas_da_unidade", "Pode editar entradas de adolescentes vinculados na mesma unidade"),
            
            ("editar_chegadas", "Pode editar chegadas previstas de adolescentes em unidades"),
            ("editar_saidas", "Pode editar saídas previstas de adolescentes em unidades"),
            
            ("incluir_entradas", "Pode incluir adolescentes em qualquer unidade"),
            (
                "incluir_entradas_na_unidade",
                "Pode incluir adolescentes na unidade em que está lotado",
            ),
            ("excluir_entradas", "Pode remover adolescentes de qualquer unidade"),
            (
                "excluir_entradas_da_unidade",
                "Pode remover adolescentes da unidade em que está lotado",
            ),
        )

    @property
    def unidade_posterior(self):
        if hasattr(self, 'vinculacao_de_saida'):
            if self.vinculacao_de_saida.unidade_destino is not None:
                return self.vinculacao_de_saida.unidade_destino
        
        if hasattr(self, 'transferencia_de_saida'):
            if self.transferencia_de_saida.unidade_destino is not None:
                return self.transferencia_de_saida.unidade_destino
        
        return None
    
    @property
    def unidade_anterior(self):
        if hasattr(self, 'vinculacao_de_entrada'):
            if self.vinculacao_de_entrada.unidade_origem is not None:
                return self.vinculacao_de_entrada.unidade_origem
        
        if hasattr(self, 'transferencia_de_entrada'):
            if self.transferencia_de_entrada.unidade_origem is not None:
                return self.transferencia_de_entrada.unidade_origem
        return None
    
    @property
    def apto_para_checkin(self):
        return not self.adolescente.entradas_em_unidades.filter(lotado=True).exists()

    @property
    def equipe_referencia(self):
        return list(
            chain(self.especialista_referencia.all(), self.agente_referencia.all())
        )

    @property
    def vinculado(self):
        return (
            self.lotado and self.tipo_vaga.descricao not in TIPOS_VAGA_NAO_VINCULANTES
        )

    @property
    def em_atividade_externa(self):
        if self.em_atividade:
            if self.atividade_atual.atividade.externa:
                return True
        return False

    
    @property
    def em_atividade(self):
        return self.adolescente.historico_atividades.filter(
            atividade__unidade=self.unidade, 
            em_atividade=True,
            data_ida__gte = self.data_entrada if self.data_entrada is not None else datetime.datetime(year=2023,month=1,day=1),
        ).exists()

    @property
    def atividade_atual(self):
        return self.adolescente.historico_atividades.filter(
            atividade__unidade=self.unidade, 
            em_atividade=True,
            data_ida__gte = self.data_entrada if self.data_entrada is not None else datetime.datetime(year=2023,month=1,day=1),
        ).first()

    @property
    def medidas_adaptacao_ativas(self):
        return self.medidas_adaptacao.filter(data_fim__gte=timezone.now())

    @property
    def tem_medida_adaptacao(self):
        return self.medidas_adaptacao_ativas.exists()

    @property
    def medidas_disciplinares_ativas(self):
        return self.medidas_disciplinares.filter(data_fim__gte=timezone.now())

    @property
    def tem_medida_disciplinar(self):
        return self.medidas_disciplinares_ativas.exists()

    def clean(self, *args, **kwargs):
        logica_entrada_em_unidade(self)
        super().clean(*args, **kwargs)

    def realizar_entrada(self):
        self.status = self.Status.ENTRADA_REALIZADA
        self.save()

    def realizar_saida(self):
        self.status = self.Status.SAIDA_REALIZADA
        self.save()


class AnexoEntrada(BaseModel):
    anexo = models.FileField(max_length=500, 
        upload_to=generate_uuid4_filename, validators=[validate_file_size]
    )
    entrada = models.ForeignKey(
        EntradaAdolescente,
        related_name="anexos",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    descricao = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Descrição",
    )


class Medida(BaseModel):
    data_inicio = models.DateField(
        blank=False,
        null=False,
        verbose_name="Data Início",
    )
    duracao = models.IntegerField(
        blank=False,
        null=False,
        verbose_name="Duração",
    )
    descricao = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Descrição",
    )
    data_fim = models.DateField(
        blank=True,
        null=False,
        editable=False,
        verbose_name="Data Fim",
    )

    def clean(self, *args, **kwargs):
        if self.duracao is not None:
            self.data_fim = self.data_inicio + datetime.timedelta(days=self.duracao)
        super().clean(*args, **kwargs)

    @property
    def ativa(self):
        return self.data_fim >= timezone.now().date() and self.duracao is not None

    def _medida_to_str(self):
        return (
            f"{self.duracao} dia(s) a partir de {self.data_inicio.strftime('%d/%m/%Y')}"
        )

    class Meta:
        abstract = True


class MedidaAdaptacao(Medida):
    entrada = models.ForeignKey(
        EntradaAdolescente, related_name="medidas_adaptacao", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.entrada.adolescente.nome}: {self._medida_to_str()}"

    class Meta:
        verbose_name = "Medida de Adaptação"
        verbose_name_plural = "Medidas de Adaptação"
        permissions = (
            ("ver_ma", "Pode ver medidas de adaptação de adolescentes em unidades"),

            ("ver_ma_da_unidade", "Pode ver medidas de adaptação de adolescentes da unidade em que está lotado."),
            

            ("editar_ma", "Pode editar medidas de adaptação de adolescentes"),
            (
                "editar_ma_da_unidade",
                "Pode editar medidas de adaptação de adolescentes da mesma unidade",
            ),
            (
                "incluir_ma",
                "Pode incluir medidas de adaptação para adolescentes em qualquer unidade",
            ),
            (
                "incluir_ma_na_unidade",
                "Pode incluir medidas de adaptação para adolescentes da unidade em que está lotado",
            ),
            (
                "excluir_ma",
                "Pode remover medidas de adaptação de adolescentes de qualquer unidade",
            ),
            (
                "excluir_ma_da_unidade",
                "Pode remover medidas de adaptação de adolescentes da unidade em que está lotado",
            ),
        )


class MedidaDisciplinar(Medida):
    entrada = models.ForeignKey(
        EntradaAdolescente,
        related_name="medidas_disciplinares",
        on_delete=models.CASCADE,
    )
    ocorrencia = models.ForeignKey(
        "ocorrencias.Ocorrencia",
        related_name="medidas_geradas",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.entrada.adolescente.nome}: {self._medida_to_str()}"

    class Meta:
        verbose_name = "Medida Disciplinar'"
        verbose_name_plural = "Medidas Disciplinares"
        permissions = (
            ("ver_md", "Pode ver medidas disciplinares de adolescentes em unidades"),
            (
                "ver_md_da_unidade",
                "Pode ver medidas disciplinares de adolescentes da unidade em que está lotado.",
            ),
            ("editar_md", "Pode editar medidas disciplinares de adolescentes"),
            (
                "editar_md_da_unidade",
                "Pode editar medidas disciplinares de adolescentes da mesma unidade",
            ),
            (
                "incluir_md",
                "Pode incluir medidas disciplinares para adolescentes em qualquer unidade",
            ),
            (
                "incluir_md_na_unidade",
                "Pode incluir medidas disciplinares para adolescentes da unidade em que está lotado",
            ),
            (
                "excluir_md",
                "Pode remover medidas disciplinares de adolescentes de qualquer unidade",
            ),
            (
                "excluir_md_da_unidade",
                "Pode remover medidas disciplinares de adolescentes da unidade em que está lotado",
            ),
        )
