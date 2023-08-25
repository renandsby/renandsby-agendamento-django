from django.db import models

class TipoRedeApoio(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Rede de Apoio"
        verbose_name_plural = "Tipos de Rede de Apoio"








