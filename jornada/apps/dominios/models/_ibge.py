from django.db import models
from geoposition.fields import GeopositionField


class Regiao(models.Model):
    nome = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.nome}'

    class Meta:
        app_label = "dominios"
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'


class Uf(models.Model):
    sigla = models.CharField(max_length=2, primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    regiao = models.ForeignKey(Regiao, on_delete=models.SET_NULL, blank=True, null=True)
    codigo = models.CharField(max_length=2, blank=True, null=True, unique=True)

    def __str__(self) -> str:
        return f'{self.nome}-{self.sigla}'
    
    class Meta:
        app_label = "dominios"
        verbose_name_plural = 'UFs'


class Cidade(models.Model):
    codigo = models.CharField(max_length=7, blank=True, primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    uf = models.ForeignKey(Uf, models.SET_NULL, blank=True, null=True, related_name="cidades")
    
    def __str__(self) -> str:
        return f'{self.nome} - {self.uf.sigla}'

    class Meta:
        ordering = ("nome",)
        app_label = "dominios"
        verbose_name_plural = 'Cidades'


class Bairro(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.ForeignKey(Cidade, models.SET_NULL, blank=True, null=True, related_name="bairros")
    codigo = models.CharField(max_length=10, blank=True, null=True, unique=True)
    localizacao = GeopositionField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.nome}'

    class Meta:
        ordering = ["nome",] 
        app_label = "dominios"
        verbose_name_plural = 'Bairros'
