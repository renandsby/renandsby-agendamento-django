from django.db import models
from core.models import BaseModel
from core.models.utils import generate_uuid4_filename
from core.validators import validate_file_size
from .base import BaseDesvinculacao, BaseVinculacao


class Transferencia(BaseDesvinculacao, BaseVinculacao):
    
    def __str__(self):
        string = f"Transferência de {self.adolescente.nome}"
        if self.unidade_origem:
            string += f" de {self.unidade_origem.sigla}"
        if self.unidade_destino:
            string += f" para {self.unidade_destino.sigla}"
        return string

    class Meta:
        app_label = "alteracoes_vinculo"
        verbose_name = "Transferência"
        verbose_name_plural = "Transferências"
        ordering = ('-criado_em', )
        permissions = (
            ("ver_transferencias", "Ver Transferências"),
            ("editar_transferencias", "Editar Transferências"),
            ("criar_transferencias", "Criar Transferências"),
            ("deletar_transferencias", "Deletar Transferências"),
        )
    
    def transferir(self):        
        try:
            self.realizar_desvinculacao()
            self.realizar_vinculacao()
        except Exception as e:
            self.desfazer()
            raise e

    def desfazer(self):
        self.desfazer_vinculacao()
        self.desfazer_desvinculacao()

class AnexoTransferencia(BaseModel):
    transferencia = models.ForeignKey(Transferencia, related_name="anexos", on_delete=models.SET_NULL, blank=True, null=True)
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(max_length=100, null=True, blank=True, verbose_name="Descrição")

