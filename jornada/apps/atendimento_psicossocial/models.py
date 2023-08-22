from django.db import models
from core.models import BaseModel, VinculaPassagemAdolescente
from core.models.utils import generate_uuid4_filename
from core.validators import validate_file_size

class AtendimentoPsicossocial(VinculaPassagemAdolescente, BaseModel):
    adolescente = models.ForeignKey(
        'adolescentes.Adolescente', 
        on_delete=models.CASCADE)
    especialidade_atendimento = models.ForeignKey(
        'dominios.EspecialidadeAtendimentoPsicossocial', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        verbose_name="Especialidade de Atendimento"
    )
    tipo_atendimento = models.ForeignKey(
        'dominios.TipoAtendimentoPsicossocial', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        verbose_name="Tipo de Atendimento"
    )
    data_atendimento = models.DateField(blank=False, null=True, verbose_name="Data de Atendimento")
    observacoes_publicas = models.TextField(blank=True, null=True, verbose_name="Observações Públicas")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações Sigilosas")

    def __str__(self) -> str:
        return f"Atendimento de {self.adolescente}"
    
    class Meta:
        ordering = ("-data_atendimento",)
        verbose_name_plural = "Atendimentos Sociopsicopedagógicos"
        verbose_name = "Atendimento Sociopsicopedagógico"
        permissions = (
            ("ver", "Pode ver parte sigilosa de Atendimentos"),
            ("editar", "Pode editar todos os atendimentos"),
            ("incluir", "Pode incluir Atendimentos"),
        )


class AnexoAtendimento(BaseModel):
    atendimento_psicossocial = models.ForeignKey(
        'AtendimentoPsicossocial', 
        on_delete=models.CASCADE, 
        related_name='anexos')
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descrição")
