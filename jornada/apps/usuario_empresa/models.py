import datetime
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

    nome = models.CharField(max_length=255, null=True)
    razao_social = models.CharField(max_length=255, null=True, unique=True)
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

   
