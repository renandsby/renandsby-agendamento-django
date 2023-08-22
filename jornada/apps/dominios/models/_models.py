from django.db import models


class JornadaTrabalho(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = "dominios"
        verbose_name = "Jornada de Trabalho"
        verbose_name_plural = "Jornadas de Trabalho"


class Cargo(models.Model):
    codigo = models.CharField(max_length=15, blank=True, primary_key=True)
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = "dominios"


class EspecialidadeAtendimentoPsicossocial(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = "dominios"
        verbose_name = "Especialidade de Atendimento Psicossocial"
        verbose_name_plural = "Especialidade de Atendimentos Psicossocial"


class TipoAtendimentoPsicossocial(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descricao

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Atendimento Psicossocial"
        verbose_name_plural = "Tipo de Atendimentos Psicossocial"

class Genero(models.Model):
    descricao = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name_plural = "Gêneros"
        verbose_name = "Gênero"


class Cor(models.Model):
    descricao = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name_plural = "Cores"


class TipoResponsavel(models.Model):
    descricao = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Responsável"
        verbose_name_plural = "Tipos de Responsável"



class TipoRedeApoio(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Rede de Apoio"
        verbose_name_plural = "Tipos de Rede de Apoio"



class Vara(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"

class TipoProcesso(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Processo"
        verbose_name_plural = "Tipos de Processo"


class AtoInfracional(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        ordering = ('id',)
        app_label = "dominios"
        verbose_name = "Ato Infracional"
        verbose_name_plural = "Atos Infracionais"


class TipoDecisaoProcesso(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Decisão em Processo"
        verbose_name_plural = "Tipos de Decisão em Processo"


class TipoEntradaUnidade(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Entrada em Unidade"
        verbose_name_plural = "Tipos de Entrada em Unidade"

class TipoSaidaUnidade(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Saída em Unidade"
        verbose_name_plural = "Tipos de Saída em Unidade"


class TipoVagaUnidade(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name_plural = "Tipos de Vaga em Unidade"


class MedidaSocioeducativa(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name_plural = "Medidas Socioeducativas"


class TipoMedida(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name_plural = "Tipos de Medida Socioeducativas"
        verbose_name = "Tipo de Medida Socioeducativa"


class OrigemEntradaUnidade(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Origem de Entrada em Unidade"
        verbose_name_plural = "Origens de Entrada em Unidade"

class TipoUnidade(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Unidade"
        verbose_name_plural = "Tipos de Unidade"


class TipoAtividade(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        ordering = ('descricao',)
        app_label = "dominios"
        verbose_name = "Tipo de Atividade"
        verbose_name_plural = "Tipos de Atividade"


class SituacaoEscolar(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Situação Escolar"
        verbose_name_plural = "Situações Escolares"


class Escolaridade(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Escolaridade"
        verbose_name_plural = "Escolaridades"


class TipoRisco(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Tipo de Risco"
        verbose_name_plural = "Tipos de Risco"


class GravidadeInfracaoOcorrencia(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Gravidade de Ocorrência"
        verbose_name_plural = "Gravidades de Ocorrência"

class RegulamentoInfracoes(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Regulamento Definidor de Infrações"
        verbose_name_plural = "Regulamentos Definidores de Infrações"

class InfracaoOcorrencia(models.Model):
    descricao = models.TextField()
    gravidade = models.ForeignKey(
        GravidadeInfracaoOcorrencia, on_delete=models.SET_NULL, null=True, blank=False
    )
    regulamento_infracoes = models.ForeignKey(
        RegulamentoInfracoes, on_delete=models.SET_NULL, null=True, blank=False, related_name='infracoes'
    )

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Infração em Ocorrência"
        verbose_name_plural = "Infrações em Ocorrências"


class CircunstanciaOcorrencia(models.Model):
    descricao = models.CharField(max_length=255)
    momento = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Circunstância em Ocorrência"
        verbose_name_plural = "Circunstâncias em Ocorrências"


class TurnoEscolar(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Turno Escolar"
        verbose_name_plural = "Turnos Escolares"



class OpcaoSabeLer(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Opção para 'Saber Ler?'"
        verbose_name_plural = "Opções para 'Saber Ler?'"


class OpcaoEncaminhadoCre(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        app_label = "dominios"
        verbose_name = "Opção para 'Encaminhado para CRE''"
        verbose_name_plural = "Opções para 'Encaminhado para CRE'"


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
