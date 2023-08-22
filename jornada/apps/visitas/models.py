from django.db import models
from core.models import BaseModel
from .logic import logica_visita

class Visita(BaseModel):
    modulo = models.ForeignKey("unidades.Modulo", null=False, blank=False, on_delete=models.CASCADE)
    adolescente = models.ForeignKey("adolescentes.Adolescente", null=True, blank=False, on_delete=models.SET_NULL)
    visitante = models.ForeignKey("adolescentes.Familiar", null=True, blank=False, on_delete=models.SET_NULL)
    data_entrada = models.DateTimeField("Data Entrada", null=True, blank=False)
    data_saida = models.DateTimeField("Data de Saída", null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    em_visita = models.BooleanField(default=False)

    def __str__(self):
        return f"Visita de {self.visitante} a {self.adolescente} em {self.data_entrada.strftime('%d/%m/%Y')}"

    def clean(self) -> None:
        logica_visita(self)
        return super().clean()
    
    class Meta:
        verbose_name_plural = "Visitas"
        verbose_name = "Visita"
        
        permissions = (
            ("ver", "Pode ver visitas"),
            ("editar", "Pode editar visitas"),
            ("registrar", "Pode registrar visitas"),
            ("excluir", "Pode excluir visitas"),
        )

class PertenceVisita(BaseModel):
    visita = models.ForeignKey(Visita, null=False, blank=False, on_delete=models.CASCADE)
    adolescente = models.ForeignKey("adolescentes.Adolescente", null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.PositiveSmallIntegerField(blank=True, null=True)
    descricao_item = models.CharField(verbose_name="Item", max_length=30, null=False, blank=False)
    data_recebimento = models.DateTimeField(null=False, blank=False)
    data_entrega = models.DateTimeField(null=True, blank=True)
    observacoes = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observações",
    )

    def clean(self) -> None:
        return super().clean()