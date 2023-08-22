from django.db import models
from core.models import BaseModel, VinculaPassagemAdolescente
from core.models.utils import generate_uuid4_filename
from core.validators import validate_file_size
# Create your models here.

class Risco(VinculaPassagemAdolescente, BaseModel):
    adolescente = models.ForeignKey('adolescentes.Adolescente', related_name='riscos', on_delete=models.CASCADE, blank=True)
    descricao = models.TextField("Descrição", blank=True, null=True)
    data_registro = models.DateField("Data de Registro")
    tipo_risco = models.ManyToManyField('dominios.TipoRisco', verbose_name="Tipos de Risco")
    ativo = models.BooleanField("Ativo" , default=False)

    def __str__(self):
        return f"Risco de {self.adolescente.nome}"

'''
TODO: lidar com upload de arquivos, servidor de arquivos proprio (pro futuro)
'''
class AnexoRisco(BaseModel):
    risco = models.ForeignKey('Risco', on_delete=models.CASCADE, related_name='anexos')
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(max_length=255, blank=True, null=True)
    
