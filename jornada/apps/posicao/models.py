from collections import defaultdict
from datetime import datetime
from xml.dom import ValidationErr
from django.db import models
from core.models import BaseModel
from geoposition.fields import GeopositionField
from dominios.models import Bairro, Cidade, Uf

class RedeEmpresas(BaseModel):
    descricao = models.CharField("Descrição curta", max_length=50)
    observacoes = models.TextField("Observações", null=True, blank=True, max_length=255)
    tipo_rede_localizacao = models.ForeignKey("dominios.TipoRedeApoio", on_delete=models.SET_NULL, null=True, verbose_name="Tipo de Posição" )

   
    def __str__(self):
        return self.descricao
    

class Endereco(BaseModel):
    redeEmpresas = models.ForeignKey(
        RedeEmpresas,
        on_delete=models.CASCADE,
    )
    uf = models.ForeignKey(Uf, on_delete=models.SET_NULL, null=True, verbose_name="UF")
    cidade = models.ForeignKey(
        Cidade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Cidade"
    )
    bairro = models.ForeignKey(
        Bairro, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Bairro"
    )
    vagasDisponiveis = models.BooleanField("Neste Endereço exitem vagas disponíveis?", default=False)
    descricao = models.CharField("Descrição", max_length=255, blank=True, null=True)
    cep = models.CharField("CEP", max_length=10, blank=True, null=True)
    logradouro = models.CharField("Logradouro", max_length=255, blank=True, null=True)
    complemento = models.CharField("Complemento", max_length=255, blank=True, null=True)
    numero = models.CharField("Número", max_length=50, blank=True, null=True)
    localizacao = GeopositionField(null=True, blank=True)
    descricao_vaga = models.CharField("Descrição Vaga", max_length=100, blank=True, null=True)
    data_agendamento_inicio = models.DateTimeField("Data Início Vaga", null=True, blank=True)
    data_agendamento_final = models.DateTimeField("Data de Final Vaga", null=True, blank=True)
    departamento = models.CharField("Departamento", max_length=20)
    sala = models.CharField("Sala", max_length=20)
    mesa = models.CharField("Mesa", max_length=20)
    
    def __str__(self):
        return f"{self.redeEmpresas} - {self.descricao_vaga}"

 
class Vagas(BaseModel):


    endereco = models.ForeignKey(
        Endereco, on_delete=models.CASCADE
    )
    # data_agendamento_inicio = models.DateTimeField("Data Início", null=True, blank=False)
    # data_agendamento_final = models.DateTimeField("Data de Final", null=True, blank=True)
    # departamento = models.CharField("Departamento", max_length=20)
    # sala = models.CharField("Sala", max_length=20)
    # mesa = models.CharField("Mesa", max_length=20)
    descricao = models.CharField("Descrição", max_length=100, blank=True, null=True)
    
    # def clean(self):
    #     if self.data_agendamento_inicio < datetime.now():
    #         raise ValidationErr("Não é permitido cadastrar eventos em datas passadas.")
    #     return self.clean()
       

    def __str__(self):
        return f"{self.descricao}"



