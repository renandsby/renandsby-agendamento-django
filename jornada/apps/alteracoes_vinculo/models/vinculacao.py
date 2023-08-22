from django.db import models
from core.models import BaseModel
from core.models.utils import generate_uuid4_filename
from core.validators import validate_file_size
from .base import BaseVinculacao, BaseDesvinculacao



class Vinculacao(BaseDesvinculacao, BaseVinculacao):
    def __str__(self):
        string = f"Vinculacao de {self.adolescente.nome}"
        if self.unidade_destino:
            string += f" em {self.unidade_destino.sigla}"
        return string
    
    def vincular(self):
        try:
            self.realizar_desvinculacao()
            self.realizar_vinculacao()
        except Exception as e:
            self.desfazer()
            raise e
    
    def desfazer(self):
        self.desfazer_vinculacao()
        self.desfazer_desvinculacao()
        
    class Meta:
        app_label = "alteracoes_vinculo"
        verbose_name = 'Vinculação'
        verbose_name_plural = 'Vinculações'
        ordering = ('-criado_em', )
        permissions = (
            ("ver_vinculacoes", "Ver Vinculações"),
            ("editar_vinculacoes", "Editar Vinculações"),
            ("criar_vinculacoes", "Criar Vinculações"),
            ("deletar_vinculacoes", "Deletar Vinculações"),
        )

    


class AnexoVinculacao(BaseModel):
    vinculacao = models.ForeignKey(Vinculacao, related_name="anexos", on_delete=models.SET_NULL, blank=True, null=True)
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(max_length=100, null=True, blank=True, verbose_name="Descrição")