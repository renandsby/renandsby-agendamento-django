from django import forms
from itertools import chain
from core.models import BaseModel, VinculaPassagemAdolescente
from core.models.utils import generate_uuid4_filename
from django.db import models
from dominios.models import SimNao, SituacaoEscolar
from core.validators import (
    CaracteresEspeciaisValidator, 
    SomenteNumeros,
    cidade_do_uf, 
    valida,
    validate_file_size
)


class Pia(VinculaPassagemAdolescente, BaseModel):

    caracter_especial_validator = CaracteresEspeciaisValidator()

    adolescente = models.ForeignKey('adolescentes.Adolescente', on_delete=models.CASCADE, blank=True, related_name='pias')
    unidade = models.ForeignKey("unidades.Unidade", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="pias")
   
    servidor_referencia = models.ForeignKey("servidores.Servidor", blank=True,null=True,on_delete=models.SET_NULL, verbose_name="Servidor Referencia", related_name="pias_como_servidor_referencia")
    tecnico_1 = models.ForeignKey("servidores.Servidor", blank=True,null=True,on_delete=models.SET_NULL, verbose_name="Técnico 1", related_name="pias_como_tecnico_1")
    tecnico_2 = models.ForeignKey("servidores.Servidor", blank=True,null=True,on_delete=models.SET_NULL, verbose_name="Técnico 2", related_name="pias_como_tecnico_2")
    tecnico_3 = models.ForeignKey("servidores.Servidor", blank=True,null=True,on_delete=models.SET_NULL, verbose_name="Técnico 3", related_name="pias_como_tecnico_3")

    data_atendimento = models.DateField(blank=False, null=True, verbose_name="Data de Atendimento")
    levantamento_contexto_familiar = models.TextField("Levantamento de Contexto Familiar", blank=True, null=True)
    composicao_familiar = models.TextField("Composição Familiar", blank=True, null=True)
    renda_familiar = models.CharField("Renda Familiar",max_length=7, blank=True, null=True)
    qtd_integrantes_familiar = models.CharField("Quantidade de Integrantes Familiar", max_length=3,blank=True, null=True)
    qtd_filhos_adolescente = models.CharField("Quantidade de filhos do adolescente",max_length=3, blank=True, null=True)
    historico_infracional = models.TextField("Histórico Infracional", blank=True, null=True)

    historico_clinico = models.TextField("Histórico Clínico", blank=True, null=True)
    diagnostico_da_equipe_saude = models.TextField("Diagnóstico Situacional e as percepções da equipe", blank=True, null=True)
    metas_e_objetivos_adolescente_saude = models.TextField("Metas e Objetivos declarados pelos adolescente", blank=True, null=True)
    avaliacao_de_especialista = models.CharField("Avaliação de especialista", choices=SimNao.choices, max_length=3, blank=True, null=True)

    descricao_avaliacao_especialista = models.CharField(
        "Qual", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    
    uso_de_drogas = models.CharField("Usa Drogas", choices=SimNao.choices, max_length=3, blank=True, null=True)

    descricao_uso_de_drogas = models.CharField(
        "Qual tipo de droga:", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    uf = models.ForeignKey(
        "dominios.Uf",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name="UF",
    )
    cidade = models.ForeignKey(
        "dominios.Cidade", on_delete=models.DO_NOTHING, blank=True, null=True,
    )


    # Iniciacao profissional

    situacao_profissional = models.CharField(
        "Situação profissional", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    tem_curriculo= models.CharField("Tem Curriculo", choices=SimNao.choices, max_length=3, blank=True, null=True)

    ja_participou_de_curso = models.CharField("Ja Participou de algum curso", choices=SimNao.choices, max_length=3, blank=True, null=True)

    descricao_cursos = models.CharField(
        "Qual tipo de curso", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    diagnostico_situacional_da_equipe_profissionalizacao = models.TextField("Metas e Objetivos declarados pelos adolescentes", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_profissionalizacao = models.TextField("Metas e Objetivos declarados pelos adolescentes", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_profissionalizacao = models.TextField("Metas e Objetivos declarados pelos adolescentes", blank=True, null=True)
    




    # Religião
    crenca = models.CharField(
        "Crença", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    diagnostico_situacional_da_equipe_religiao = models.TextField("Diagnósticos Situacional e as Percepções da Equipe", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_religiao = models.TextField("Metas e Objetivos declarados pelos adolescente", blank=True, null=True)

    # RELAÇÕES AFETIVAS DE AMIZADE E DE GÊNERO
    relacao_afetiva = models.CharField(
        "Informações", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    diagnostico_situacional_da_equipe_relacao_afetiva = models.TextField("Diagnósticos Situacional e as Percepções da Equipe", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_relacao_afetiva = models.TextField("Metas e Objetivos declarados pelos adolescente", blank=True, null=True)

    # LAZER
    lazer = models.CharField(
        "Informações", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    diagnostico_situacional_da_equipe_lazer = models.TextField("Diagnósticos Situacional e as Percepções da Equipe", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_lazer = models.TextField("Metas e Objetivos declarados pelos adolescente", blank=True, null=True)

    # Cultura
    cultura = models.CharField(
        "Informações", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    diagnostico_situacional_da_equipe_cultura = models.TextField("Diagnósticos Situacional e as Percepções da Equipe", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_cultura = models.TextField("Metas e Objetivos declarados pelos adolescente", blank=True, null=True)

    # Esporte
    esporte = models.CharField(
        "Informações", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    diagnostico_situacional_da_equipe_esporte = models.TextField("Diagnósticos Situacional e as Percepções da Equipe", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_esporte = models.TextField("Metas e Objetivos declarados pelos adolescente", blank=True, null=True)

    # Integração Familiar  
    integracao_familiar = models.CharField(
        "Informações", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    diagnostico_situacional_da_equipe_integracao_familiar = models.TextField("Diagnósticos Situacional e as Percepções da Equipe", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_integracao_familiar = models.TextField("Metas e Objetivos declarados pelos adolescente", blank=True, null=True)



    # Programas do Governo 
    programas_governo = models.CharField(
        "Informações", max_length=100, validators=[caracter_especial_validator], blank=True, null=True
    )
    diagnostico_situacional_da_equipe_governo = models.TextField("Diagnósticos Situacional e as Percepções da Equipe", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_governo = models.TextField("Metas e Objetivos declarados pelos adolescente", blank=True, null=True)



    # ACOMPANHAMENTO DO PERCUSO DO ADOLESCENTE 
    consideracao_equipe_referencia = models.TextField("Considerações da Equipe Multidisciplinar de Referência", blank=True, null=True)
    registro_de_incidente = models.TextField("Registro de Incidente Disciplinares", blank=True, null=True)
    visita_familiares_domiciliares = models.TextField("Visitas Familiares Domiciliares", blank=True, null=True)
    registro_fatos_positivos = models.TextField("Registro de Fatos Positivos", blank=True, null=True)
    atividades_interna_regras_institucionais = models.TextField("Atividades Internas - Respeito as Regras institucionais", blank=True, null=True)
    atividade_externa_participacao_atividades = models.TextField("Atividades Externas - Participação em Atividades", blank=True, null=True)
    atividade_integracao_familiar = models.TextField("Atividades de Integração Familiares", blank=True, null=True)
    medidades_saude = models.TextField("Medidas de Atenção a Saúde", blank=True, null=True)
    parecer_tecnico = models.TextField("Parecer Técnico Interdisciplinar", blank=True, null=True)



    #Educacao
    situacao_escolar = models.ForeignKey(
        "dominios.SituacaoEscolar", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    escolaridade = models.ForeignKey(
        "dominios.Escolaridade", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    endereco_escola = models.CharField("Endereço da Escola",max_length=255, blank=True, null=True)
    motivo_desistencia = models.CharField("Motivo",max_length=255, blank=True, null=True)
    historico_escolar = models.CharField("Historico Escolar",max_length=255, blank=True, null=True)
    avaliacao_pedagica = models.CharField("Avaliação Psicopedagógica",max_length=255, blank=True, null=True)
  
    diagnostico_situacional_da_equipe_educacao = models.TextField("Diagnósticos Situacional e as Percepções da Equipe", blank=True, null=True)
    metas_e_objetivos_profissionais_adolescente_educacao = models.TextField("Metas e Objetivos Declarados Pelos Adolescente", blank=True, null=True)
    alfabetizado = models.CharField("Alfabetizado", choices=SimNao.choices, max_length=3, blank=True, null=True)
    matriculado = models.CharField("Matriculado", choices=SimNao.choices, max_length=3, blank=True, null=True)
    tem_carteirinha = models.CharField(choices=SimNao.choices, max_length=3, blank=True, null=True, verbose_name="Tem carteirinha de estudante")

    desistencia = models.CharField("Desistencia", choices=SimNao.choices, max_length=3, blank=True, null=True)

    def __str__(self):
        return f"PIA {self.id} de {self.adolescente.nome} da unidade: {self.unidade}"
    
class AnexoPia(BaseModel):
    anexo_pia = models.ForeignKey(
        Pia, 
        on_delete=models.CASCADE, 
        related_name='anexos')
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Descrição",
    )

    def __str__(self):
        return f"{self.descricao}"
