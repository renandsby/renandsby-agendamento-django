from xml.dom import VALIDATION_ERR, ValidationErr
from core.models import BaseModel
from datetime import datetime, timedelta
from django.db import models
from core.models.utils import generate_uuid4_filename
from .logic import logica_agendamento
from posicao.models import Endereco

class Agendamento(BaseModel):
    data_disponibilidade = models.DateTimeField("Data do agendamento")

    vagaEndereco = models.ForeignKey(
        Endereco, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Escolha seu agendamento"
    )
    titulo = models.CharField(max_length=100)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    # def clean(self):
    #     # Obtém a data de hoje e as datas mínima e máxima permitidas
    #     data_hoje = datetime.now()
    #     data_minima = data_hoje + timedelta(days=1)
    #     data_maxima = data_hoje + timedelta(days=7)

    #     if self.data_inicio.date() < data_minima:
    #        raise VALIDATION_ERR("Você só pode agendar para D+1.")
       
    #     if self.data_inicio.date() > data_maxima:
    #        raise VALIDATION_ERR("Você só pode agendar até D+7.")
       
    #     return  self.clean()
    
    # def save(self, *args, **kwargs):
        # self.clean()
        # super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Agendamentos"
        verbose_name = "Agendamento"


