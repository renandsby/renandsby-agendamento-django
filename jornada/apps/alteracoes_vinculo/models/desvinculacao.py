from django.db import models
from core.models import BaseModel
from core.models.utils import generate_uuid4_filename
from core.validators import validate_file_size
from .base import BaseDesvinculacao


class Desvinculacao(BaseDesvinculacao):
    def __str__(self):
        string = f"Desvinculação de {self.adolescente.nome}"
        if self.unidade_origem:
            string += f" de {self.unidade_origem.sigla}"
        return string

    def desvincular(self):
        
        try:
            self.realizar_desvinculacao()
        except Exception as e:
            self.desfazer()
            raise e
    
    def desfazer(self):
        self.desfazer_desvinculacao()

    class Meta:
        app_label = "alteracoes_vinculo"
        verbose_name = 'Desvinculação'
        verbose_name_plural = 'Desvinculações'
        ordering = ('-criado_em', )
        permissions = (
            ("ver_desvinculacoes", "Ver Desvinculações"),
            ("editar_desvinculacoes", "Editar Desvinculações"),
            ("criar_desvinculacoes", "Criar Desvinculações"),
            ("deletar_desvinculacoes", "Deletar Desvinculações"),
        )
            

class AnexoDesvinculacao(BaseModel):
    desvinculacao = models.ForeignKey(Desvinculacao, related_name="anexos", on_delete=models.SET_NULL, blank=True, null=True)
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(max_length=100, null=True, blank=True, verbose_name="Descrição")