from adolescentes.models import Adolescente
from core.models import BaseModel
from core.models.utils import generate_uuid4_filename
from django.core.exceptions import ValidationError
from django.db import models
from core.validators import validate_file_size


class Processo(BaseModel):
    class Status(models.IntegerChoices):
        ATIVO = 1, "Ativo"
        CUMPRIDO = 2, "Cumprido"
        EXTINTO = 3, "Extinto"
        INATIVO = 4, "Inativo"

    adolescente = models.ForeignKey(
        Adolescente,
        models.CASCADE,
        related_name="processos",
    )
    numero = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Número do Processo",
    )
    numero_paai = models.CharField(
        "Número PAAI",
        max_length=100,
        blank=True,
        null=True,
    )
    data_apreensao = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Data Da Apreensão",
    )
    data_sentenca = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Data Da Sentença"
    )
    
    observacoes = models.TextField(blank=True, null=True)
    tipo_processo = models.ForeignKey(
        "dominios.TipoProcesso",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tipo De Processo",
    )
    origem_paai = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Origem PAAI"
    )
    vara = models.ForeignKey(
        "dominios.Vara", on_delete=models.SET_NULL, null=True, blank=True
    )
    nr_pia = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Número PIA"
    )

    atos_infracionais = models.ManyToManyField("dominios.AtoInfracional", blank=True)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.ATIVO
    )


    def str_sem_nome(self):
        if self.numero:
            return str(self.numero)
        if self.numero_paai:
            return "(PAAI)"+str(self.numero_paai)
        
    def __str__(self):
        return f"{self.adolescente.nome} - {self.str_sem_nome()}"

    class Meta:
        ordering = ('status',)
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_numero_or_numero_paai",
                check=(
                    models.Q(numero__isnull=False) | models.Q(numero_paai__isnull=False)
                ),
                violation_error_message="É necessário preencher ao menos um dos campos: 'Número Processo' ou 'Número PAAI'",
            )
        ]
        permissions = (
            ("ver", "Pode ver processos"),
            ("ver_da_unidade", "Pode ver processos de adolescentes vinculados na mesma unidade"),
            
            ("editar", "Pode editar processos"),
            ("editar_da_unidade", "Pode editar processos de adolescentes vinculados na mesma unidade"),
            
            ("incluir", "Pode incluir processos"),
        )
        

class Decisao(BaseModel):
    processo = models.ForeignKey(Processo, models.CASCADE, related_name="decisoes")
    data = models.DateField(blank=True, null=True)
    tipo_decisao = models.ForeignKey(
        "dominios.TipoDecisaoProcesso", models.SET_NULL, blank=True, null=True
    )
    medida = models.ForeignKey(
        "dominios.MedidaSocioeducativa",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


class AnexoProcesso(BaseModel):
    processo = models.ForeignKey(
        Processo,
        models.CASCADE,
        related_name="anexos",
    )
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Descrição",
    )
