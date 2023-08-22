from core.models import BaseModel, VinculaPassagemAdolescente
from core.validators import SomenteNumeros, cidade_do_uf, valida, validate_file_size
from core.models.utils import generate_uuid4_filename
from django.db import models


class AtendimentoEducacao(VinculaPassagemAdolescente, BaseModel):

    somente_numeros_validator = SomenteNumeros()

    data_atendimento = models.DateField(blank=True, null=True)

    sabe_ler = models.ForeignKey(
        "dominios.OpcaoSabeLer",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name="Sabe Ler",
    )

    situacao_escolar = models.ForeignKey(
        "dominios.SituacaoEscolar", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    turno_escolar = models.ForeignKey(
        "dominios.TurnoEscolar", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    escolaridade = models.ForeignKey(
        "dominios.Escolaridade", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    encaminhado_cre = models.ForeignKey(
        "dominios.OpcaoEncaminhadoCre",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name="Encaminhado para CRE",
    )

    nome_escola = models.CharField(max_length=255, blank=True, null=True)

    uf = models.ForeignKey(
        "dominios.Uf",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name="UF",
    )

    cidade = models.ForeignKey(
        "dominios.Cidade", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    bairro = models.ForeignKey(
        "dominios.Bairro", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    i_educar = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    observacoes = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    adolescente = models.ForeignKey(
        "adolescentes.Adolescente",
        on_delete=models.CASCADE,
        blank=True,
        related_name="atendimento_educacao",
    )

    @valida(cidade_do_uf)
    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

    def __str__(self) -> str:
        return f"Atendimento em Educacao #{self.pk} de {self.adolescente}"

    class Meta:
        verbose_name_plural = "Atendimentos em Educação"
        verbose_name = "Atendimento em Educação"
        ordering = ("-data_atendimento",)


class AnexoEducacao(BaseModel):
    atendimento_educacao = models.ForeignKey(
        "AtendimentoEducacao", on_delete=models.CASCADE, related_name="anexos"
    )
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Descrição",
    )
