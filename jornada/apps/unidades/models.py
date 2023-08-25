import datetime
from itertools import chain

from core.models import BaseModel
from core.models.utils import generate_uuid4_filename
from core.utils import TIPOS_VAGA_NAO_VINCULANTES
from core.validators import validate_file_size
from django.db import models
from django.db.models.functions import Cast
from django.utils import timezone
from geoposition.fields import GeopositionField

from .logic import logica_entrada_em_unidade


class Unidade(BaseModel):
    nome = models.CharField(max_length=255, null=True)
    sigla = models.CharField(max_length=255, null=True, unique=True)
    tipo_unidade = models.ForeignKey(
        "dominios.TipoUnidade", on_delete=models.SET_NULL, null=True
    )
    cep = models.CharField("CEP", max_length=8, blank=True, null=True)
    logradouro = models.CharField("Logradouro", max_length=255, blank=True, null=True)
    complemento = models.CharField("Complemento", max_length=255, blank=True, null=True)
    numero = models.CharField("Número", max_length=50, blank=True, null=True)
    uf = models.ForeignKey(
        "dominios.Uf",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="UF",
    )
    cidade = models.ForeignKey(
        "dominios.Cidade",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name="Cidade",
    )
    bairro = models.ForeignKey(
        "dominios.Bairro",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name="Bairro",
    )
    localizacao = GeopositionField(null=True, blank=True)




    @property
    def agentes(self):
        return self.servidores.filter(
            cargo__descricao__in=["TSOCIO - AGENTE SOCIAL", "AGENTE SOCIOEDUCATIVO"]
        )

    @property
    def especialistas(self):
        return self.servidores.filter(cargo__descricao__startswith="ESOCIO")

    



    @property
    def vagas_disponiveis(self):
        ocupadas = self.vagas_ocupadas
        disponiveis = {}

        for vaga in self.vagas_unidade.all():
           
            if tipo not in disponiveis:
                disponiveis[tipo] = vaga.quantidade
                if tipo in ocupadas:
                    disponiveis[tipo] -= ocupadas[tipo]

        return disponiveis

    @property
    def resumo_vagas(self):
        ocupadas = self.vagas_ocupadas
        disponiveis = self.vagas_disponiveis
        resumo = {}
        for vaga in self.vagas_unidade.all():
           
            if tipo not in resumo:
                resumo[tipo] = {
                    "total": vaga.quantidade,
                    "ocupadas": 0,
                    "disponiveis": vaga.quantidade,
                }

            if tipo in ocupadas:
                resumo[tipo]["ocupadas"] = ocupadas[tipo]

            if tipo in disponiveis:
                resumo[tipo]["disponiveis"] = disponiveis[tipo]

        for tipo in ocupadas:
            if tipo not in resumo and tipo not in disponiveis:
                resumo[tipo] = {
                    "total": 0,
                    "ocupadas": ocupadas[tipo],
                    "disponiveis": 0,
                }

        return resumo


    
 
    def __str__(self):
        return f"{self.sigla}"

    class Meta:
        ordering = ["sigla"]
        permissions = (
            ("acessar_todas", "Pode acessar o sistema de todas unidades"),
            ("acessar_todas_semiliberdades", "Pode acessar o sistema de todas unidades de Semiliberdade"),
            ("acessar_todas_geamas", "Pode acessar o sistema de todas unidades de Meio Aberto"),
            ("acessar_todas_internacoes", "Pode acessar o sistema de todas unidades de Internação"),
            ("editar_unidades", "Pode editar informações de unidades"),
            ("incluir_unidades", "Pode criar novas unidades"),
        )


class VagaUnidade(models.Model):
    unidade = models.ForeignKey(
        Unidade, on_delete=models.CASCADE, related_name="vagas_unidade"
    )
  
    quantidade = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.unidade}"

    class Meta:
   
        verbose_name_plural = "Vagas na Unidade"
        permissions = (
            ("ver_vagas", "Pode ver vagas de unidades"),
            ("editar_vagas", "Pode editar vagas de unidades"),
            ("incluir_vagas", "Pode criar novas vagas em unidades"),
        )


class Modulo(BaseModel):
    unidade = models.ForeignKey(
        Unidade, on_delete=models.CASCADE, related_name="modulos"
    )
    descricao = models.CharField(max_length=30)

    class Meta:
        unique_together = ("descricao", "unidade")
        ordering = ["unidade", "descricao"]
    
    @property
    def numero_modulo(self):
        return f"Módulo {self.descricao}"

    def __str__(self):
        if self.unidade.modulos.count() == 1:
            return f"Módulo {self.unidade}"
        return f"{self.unidade} - Módulo {self.descricao}"



    




        
    class Meta:
        ordering = ["descricao"]
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique",
                fields=["unidade", "descricao"],
            ),
        ]
        


class Quarto(BaseModel):
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="quartos",
    )
    numero = models.PositiveSmallIntegerField(verbose_name="Número do Quarto")
    nome = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Nome do Quarto (Opcional)"
    )
    vagas = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        if self.modulo.unidade.modulos.count() == 1:
            return f"{self.modulo.unidade.sigla} Quarto {self.numero}{self.nome}"
        return f"{self.modulo.unidade.sigla} Modulo {self.modulo.descricao} Quarto {self.numero}{self.nome}"


    
 

    def clean(self):
        return super().clean()

    class Meta:
        ordering = ["modulo__unidade", "modulo", "numero", "nome"]
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_com_nome",
                fields=["modulo", "numero", "nome"],
            ),
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_sem_nome",
                fields=["modulo", "numero"],
                condition=models.Q(nome=None),
            ),
        ]
