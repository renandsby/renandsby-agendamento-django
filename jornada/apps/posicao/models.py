from django.db import models
from core.models import BaseModel
from geoposition.fields import GeopositionField

class RedeDeLocalizacao(BaseModel):
    descricao = models.CharField("Descrição curta", max_length=50)
    observacoes = models.TextField("Observações", null=True, blank=True, max_length=255)
    tipo_rede_localizacao = models.ForeignKey("dominios.TipoRedeApoio", on_delete=models.SET_NULL, null=True, verbose_name="Tipo Rede de Localização" )
    cep = models.CharField("CEP", max_length=8, blank=True, null=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True, null=True)
    complemento = models.CharField("Complemento", max_length=255, blank=True, null=True)
    numero = models.CharField("Número", max_length=50, blank=True, null=True)
    uf = models.ForeignKey("dominios.Uf", on_delete=models.SET_NULL, null=True, blank=False, verbose_name="UF")
    cidade = models.ForeignKey("dominios.Cidade", on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Cidade")
    bairro = models.ForeignKey("dominios.Bairro", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Bairro")
    localizacao = GeopositionField(null=True, blank=True)
    data_agendamento_inicio = models.DateTimeField("Data Início", null=True, blank=False)
    data_agendamento_final = models.DateTimeField("Data de Final", null=True, blank=True)
    departamento = models.CharField("Departamento", max_length=20)
    sala = models.CharField("Sala", max_length=20)
    mesa = models.CharField("Mesa", max_length=20)
    
    def __str__(self):
        return self.descricao