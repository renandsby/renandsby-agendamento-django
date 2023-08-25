from django.db import models




class Cargo(models.Model):
    codigo = models.CharField(max_length=15, blank=True, primary_key=True)
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = "dominios"


class TipoUnidade(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Unidade"
        verbose_name_plural = "Tipos de Unidade"






class TipoRedeApoio(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Rede de Apoio"
        verbose_name_plural = "Tipos de Rede de Apoio"








class TipoOrigem(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Origem"
        verbose_name_plural = "Tipos de Origem"


class SimNao(models.TextChoices):
    SIM = 'Sim', 'Sim'
    NAO = 'Não', 'Não'
