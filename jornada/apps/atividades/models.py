from django.db import models
from django.utils import timezone
from core.models import BaseModel
from core.models.utils import generate_uuid4_filename
from core.validators import raise_validation_error, validate_file_size
from .logic import logica_historico_atividade

class AdolescenteAtividade(BaseModel):
    """
    Tabela auxiliar que atribui atividades a adolescentes.
    """
    class Turno(models.IntegerChoices):
        MATUTINO = 1, 'Matutino'
        VESPERTINO = 2, 'Vespertino'
        MATUTINO_E_VESPERTINO = 3, 'Matutino e Vespertino'
        NOTURNO = 4, 'Noturno'
    
    turno = models.PositiveSmallIntegerField(choices=Turno.choices, blank=True, null=True)
    entrada = models.ForeignKey('unidades.EntradaAdolescente', on_delete=models.CASCADE, related_name = 'atividades_inscrito')
    atividade = models.ForeignKey('atividades.Atividade', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('entrada', 'atividade')
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_com_turno",
                fields=["atividade", "entrada", "turno"],
                violation_error_message="Adolescente já inscrito na atividade"
            ),
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_sem_turno",
                fields=["atividade", "entrada"],
                condition=models.Q(turno=None),
                violation_error_message="Adolescente já inscrito na atividade"
            ),
        ]
        permissions = (
            ("ver_inscricoes", "Pode ver inscrições de adolescentes em atividades"),
            ("editar_inscricoes", "Pode editar inscrições de adolescentes em atividades"),
            ("incluir_inscricoes", "Pode inscrever adolescentes em atividades"),
            ("excluir_inscricoes", "Pode desinscrever adolescentes de atividades"),
        )



class Atividade(BaseModel):
    """
    Atividades Internas desenvolvidas pelos Adolescentes dentro das Unidades
    """

    unidade = models.ForeignKey('unidades.Unidade', on_delete=models.CASCADE, related_name='atividades')
    descricao = models.CharField("Descrição", max_length=255, null=False, blank=False)
    nome_curto = models.CharField(max_length=20, null=False, blank=False)
    tipo_atividade = models.ManyToManyField('dominios.TipoAtividade', blank=True)
    adolescentes_inscritos = models.ManyToManyField('unidades.EntradaAdolescente', blank=True, through=AdolescenteAtividade)
    externa = models.BooleanField(default=False)
    exclusiva_inscritos = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.descricao}"
    
    def adolescentes_na_atividade(self):
        return self.historico.filter(em_atividade=True)  
    
    def adolescentes_na_atividade_modulo(self, modulo):
        entradas_atuais = modulo.entradas_atuais
        
        # todos os adolescentes do módulo que estão em atividade
        hist =  self.historico.filter(
            em_atividade=True, 
            adolescente__in=modulo.adolescentes.all(),
        )
        
        # trata o caso de adolescentes que podem ter passado mais de uma vez pela mesma unidade
        # ou seja: desconsidera atividades realizadas pelo adolescente em passagens anteriores
        ids_atuais = []
        for h in hist:
            if entradas_atuais.filter(adolescente=h.adolescente, data_entrada__lt = h.data_ida).exists():
                ids_atuais.append(h.id)
        return HistoricoAtividade.objects.filter(id__in=ids_atuais)
                
            
        
    class Meta:
        unique_together = ('unidade', 'descricao')
        permissions = (
            ("ver", "Pode ver atividades"),
            ("ver_da_unidade", "Pode ver atividades da mesma unidade"),
            
            ("editar", "Pode editar atividades"),
            ("editar_da_unidade", "Pode editar atividades da mesma unidade"),
            
            ("incluir", "Pode incluir atividades"),
            ("incluir_na_unidade", "Pode incluir atividades na mesma unidade"),
        
            ("excluir", "Pode excluir atividades"),
            ("excluir_da_unidade", "Pode excluir atividades da mesma unidade"),
        )
    


class HistoricoAtividade(BaseModel):
    """
    Tabela que mostra o histórico de atividades.
    Pra cada ida de adolescente em uma atividade, um registro é criado
    TODO mudar as regras para enviar adolescente pra atividade:
    quando o adolescente já está em outra unidade, remover ele da outra atividade automaticamente
    com horario de retorno igual ao horario da atividade que está sendo criada.
    """

    atividade = models.ForeignKey(
        Atividade, on_delete=models.SET_NULL, null=True, blank=False, related_name='historico'
    )

    adolescente = models.ForeignKey(
        'adolescentes.Adolescente', on_delete=models.CASCADE, related_name='historico_atividades'
    )
    modulo = models.ForeignKey('unidades.Modulo', on_delete=models.SET_NULL, null=True, blank=True, related_name='historico_atividades')
    data_ida = models.DateTimeField(verbose_name="Data/Hora de Ida", null=True, blank=True)
    data_retorno = models.DateTimeField(verbose_name="Data/Hora de Retorno", null=True, blank=True)
    em_atividade = models.BooleanField(default=True, editable=False)
    observacoes = models.TextField(verbose_name="Observações",default='', null=True, blank=True)
    realizada = models.BooleanField(default=False)
    retorno_indeterminado = models.BooleanField(default=False)
    
    
    # Dados Agendamento
    data_prevista_ida = models.DateTimeField(null=True, blank=True, verbose_name="Data prevista de Ida")
    observacoes_agendamento = models.TextField(default='', null=True, blank=True, verbose_name="Observações de Agendamento")
    servidores_relacionados = models.ManyToManyField('servidores.Servidor',  blank=True, verbose_name="Servidores Envolvidos")
    agendado = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.atividade} - {self.adolescente} Ida:{self.data_ida}" + (
            f" Retorno:{self.data_retorno}" if self.data_retorno else ''
        )

    
    def clean(self, *args, **kwargs):
        logica_historico_atividade(self)
        super().clean(*args, **kwargs)
    
    
    @property
    def nao_realizada(self):
        return (self.data_prevista_ida.date() < timezone.now().date()) and not self.realizada

    class Meta:
        permissions = (
            ("ver_historico", "Pode ver idas/retornos de adolescentes em atividades"),
            ("ver_historico_da_unidade", "Pode ver idas/retornos de adolescentes em atividades da mesma unidade"),
            
            ("editar_historico", "Pode editar idas/retornos de adolescentes em atividades"),
            ("editar_historico_da_unidade", "Pode editar idas/retornos de adolescentes em atividades da mesma unidade"),
            
            ("agendar", "Pode criar agendamentos de adolescentes em atividades"),
            ("movimentar", "Pode enviar/retornar adolescentes para/de atividades"),
            
            ("excluir_historico", "Pode excluir idas/retornos de adolescentes em atividades"),
            ("excluir_historico_da_unidade", "Pode excluir idas/retornos de adolescentes em atividades da mesma unidade"),
        )


class AnexoHistoricoAtividade(BaseModel):
    historico = models.ForeignKey('atividades.HistoricoAtividade', on_delete=models.CASCADE, related_name="anexos")
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size], blank=False, null=True)
    descricao = models.CharField(max_length=50, blank=True, null=True)
