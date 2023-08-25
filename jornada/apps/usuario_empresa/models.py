
from itertools import chain

from core.models import BaseModel
from django.db import models
from django.db.models.functions import Cast
from django.utils import timezone
from geoposition.fields import GeopositionField

from core.validators import (
    CaracteresEspeciaisValidator, 
    SomenteNumeros,
    cidade_do_uf, 
    valida, 
    validate_file_size
)


class UsuarioEmpresa(BaseModel):
    somente_numeros_validator = SomenteNumeros()
    caracter_especial_validator = CaracteresEspeciaisValidator()

    nome = models.CharField(max_length=255, null=True, blank=True)
    razao_social = models.CharField(max_length=255, null=True, blank=True)
    redeEmpresas = models.ForeignKey("posicao.RedeEmpresas", verbose_name="Empresas", on_delete=models.SET_NULL, null=True, blank=True, related_name="Servidores")
    user = models.OneToOneField("custom_auth.CustomUser", on_delete=models.SET_NULL, related_name="usuarioEmpresa", null=True, blank=True)
    cpf = models.CharField(
        "CPF",
        max_length=11,
        blank=True,
        null=True,
        unique=True,
        validators=[somente_numeros_validator],
    ) 
    cnpj = models.CharField(
        "CNPJ",
        max_length=11,
        blank=True,
        null=True,
        unique=True,
        validators=[somente_numeros_validator],
    )

    def __str__(self):
        return f" {self.nome} ou {self.razao_social} do user {self.user}"