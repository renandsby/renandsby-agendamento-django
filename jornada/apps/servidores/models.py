from django.db import models
from core.models import BaseModel
from datetime import datetime


class Plantao(models.IntegerChoices):
        PLANTAO_1 = 1, 'Plantão 1'
        PLANTAO_2 = 2, 'Plantão 2'
        PLANTAO_3 = 3, 'Plantão 3'
        PLANTAO_4 = 4, 'Plantão 4'
        
        @staticmethod
        def date_to_plantao(date):
            if isinstance(date, datetime):
                date = date.date()
            int_plantao = (date - datetime(1990,3,16).date()).days%4 + 1
            return Plantao(int_plantao)
        
        
        
class Servidor(BaseModel):
    class Sexo(models.TextChoices):
        FEMININO = 'F', 'Feminino'
        MASCULINO = 'M', 'Masculino'
        NAO_INFORMADO = 'N', 'Não Informado'
        
    nome = models.CharField("Nome", max_length=200, blank=True, null=True)
    matricula = models.CharField("Matrícula", max_length=8, blank=True, null=True)
    codigo_lotacao = models.CharField("Código Lotação", max_length=20, blank=True, null=True)
    descricao_lotacao = models.CharField("Descrição Lotação", max_length=100, blank=True, null=True)
    sexo = models.CharField("Sexo", choices=Sexo.choices, max_length=1, blank=True, null=True)
    data_admissao = models.DateField("Data de Admissão", blank=True, null=True)

    cargo = models.ForeignKey("dominios.Cargo", verbose_name="Cargo", on_delete=models.SET_NULL, null=True, blank=True)
    codigo_funcao = models.CharField("Código Função", max_length=20, blank=True, null=True)
    denominacao_funcao = models.CharField("Descrição Função", max_length=100, blank=True, null=True)
    jornada = models.ForeignKey("dominios.JornadaTrabalho", verbose_name="Jornada de Trabalho", on_delete=models.SET_NULL, null=True, blank=True)
    plantao = models.PositiveSmallIntegerField(choices=Plantao.choices, blank=True, null=True)
    unidade = models.ForeignKey("unidades.Unidade", verbose_name="Unidade", on_delete=models.SET_NULL, null=True, blank=True, related_name="servidores")
    user = models.OneToOneField("custom_auth.CustomUser", on_delete=models.SET_NULL, related_name="servidor", null=True, blank=True)
    
    def __str__(self):
        if self.matricula is not None:
            return self.nome+"-"+self.matricula
        return self.nome

    class Meta:
        ordering = ["nome"]
        verbose_name_plural = "Servidores"
        permissions = (
            ("ver", "Pode ver servidores"),
            ("ver_da_unidade", "Pode ver servidores lotados na mesma unidade"),
            
            ("editar", "Pode editar servidores"),
            ("editar_da_unidade", "Pode editar servidores lotados na mesma unidade"),
            
            ("incluir", "Pode incluir servidores"),
        )
