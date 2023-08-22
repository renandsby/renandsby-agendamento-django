from django.db import models
from core.models import BaseModel

class Ligacao(BaseModel):
    modulo = models.ForeignKey("unidades.Modulo", null=False, blank=False, on_delete=models.CASCADE)
    adolescente = models.ForeignKey("adolescentes.Adolescente", null=True, blank=False, on_delete=models.SET_NULL)
    telefone = models.ForeignKey("adolescentes.Telefone", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Telefones Autorizados")
    data_ligacao = models.DateTimeField("Data Ligação", null=True, blank=False)
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    

    def __str__(self):
        return f"{self.telefone}"
    
    class Meta:
        verbose_name_plural = "Ligações"
        verbose_name = "Ligação"
        
        permissions = (
            ("ver", "Pode ver ligacoes"),
            ("editar", "Pode editar ligacoes"),
            ("registrar", "Pode registrar ligacoes"),
            ("excluir", "Pode excluir ligacoes"),
        )
