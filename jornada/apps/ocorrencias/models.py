from core.models import BaseModel
from django.db import models
from core.models.utils import generate_uuid4_filename
from core.validators import validate_file_size
from .logic import logica_ocorrencia


class Ocorrencia(BaseModel):
    data_hora = models.DateTimeField("Data/Hora da Ocorrência")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição da Ocorrência")
    servidores_envolvidos = models.TextField(
        blank=True, null=True, verbose_name="Outros Servidores Envolvidos"
    )

    servidores_relacionados = models.ManyToManyField(
        "servidores.Servidor", blank=False, verbose_name="Servidores Envolvidos"
    )

    circunstancias = models.ManyToManyField(
        "dominios.CircunstanciaOcorrencia", blank=True, verbose_name="Circunstâncias"
    )

    infracoes_leves = models.ManyToManyField(
        "dominios.InfracaoOcorrencia",
        blank=True,
        verbose_name="Infrações Leves",
        related_name="ocorrencias_como_leve",
    )

    infracoes_medias = models.ManyToManyField(
        "dominios.InfracaoOcorrencia",
        blank=True,
        verbose_name="Infrações Médias",
        related_name="ocorrencias_como_media",
    )

    infracoes_graves = models.ManyToManyField(
        "dominios.InfracaoOcorrencia",
        blank=True,
        verbose_name="Infrações Graves",
        related_name="ocorrencias_como_grave",
    )

    infracoes_gravissimas = models.ManyToManyField(
        "dominios.InfracaoOcorrencia",
        blank=True,
        verbose_name="Infrações Gravíssimas",
        related_name="ocorrencias_como_gravissimas",
    )

    adolescentes_autores = models.ManyToManyField(
        "adolescentes.Adolescente", blank=False, related_name="ocorrencias_como_autor"
    )

    adolescentes_vitimas = models.ManyToManyField(
        "adolescentes.Adolescente", blank=True, related_name="ocorrencias_como_vitima"
    )

    modulo = models.ForeignKey(
        "unidades.Modulo", null=True, blank=True, on_delete=models.DO_NOTHING
    )
    unidade = models.ForeignKey(
        "unidades.Unidade", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return f"Ocorrência em {self.modulo} de {self.data_hora.strftime('%d/%m/%Y ás %H:%M')}"

    def clean(self) -> None:
        logica_ocorrencia(self)
        return super().clean()

    class Meta:
        verbose_name_plural = "Ocorrências"
        verbose_name = "Ocorrência"

        permissions = (
            ("ver", "Pode ver ocorrências"),
            (
                "ver_da_unidade",
                "Pode ver ocorrências da mesma unidade (inclui ocorrências C2/GESEG)",
            ),
            ("editar", "Pode editar ocorrências"),
            (
                "editar_da_unidade",
                "Pode editar ocorrências da mesma unidade (inclui ocorrências C2/GESEG)",
            ),
            ("incluir", "Pode incluir ocorrências"),
            (
                "incluir_na_unidade",
                "Pode incluir ocorrências na mesma unidade (inclui ocorrências C2/GESEG)",
            ),
            ("excluir", "Pode excluir ocorrências"),
            (
                "excluir_da_unidade",
                "Pode excluir ocorrências da mesma unidade (inclui ocorrências C2/GESEG)",
            ),
        )


class AnexoOcorrencia(BaseModel):
    ocorrencia = models.ForeignKey(
        "Ocorrencia", on_delete=models.CASCADE, related_name="anexos"
    )
    anexo = models.FileField(max_length=500, 
        upload_to=generate_uuid4_filename, validators=[validate_file_size]
    )
    descricao = models.CharField(max_length=50, blank=True, null=True)
