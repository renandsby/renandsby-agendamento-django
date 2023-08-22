from core.models import BaseModel
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from livro.logic import logica_criacao, logica_livro
from unidades.models import Modulo


   
class Livro(BaseModel):
    data_abertura = models.DateTimeField(
        "Data de Abertura do Livro",
        default=timezone.now,
        null=False,
        blank=False,
    )
    unidade = models.ForeignKey(
        "unidades.Unidade",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="livros",
    )
    modulo = models.ForeignKey(
        "unidades.Modulo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="livros",
    )
    servidor_passagem_anterior = models.ForeignKey(
        "servidores.Servidor",
        on_delete=models.CASCADE,
        related_name="+",
        null=False,
        blank=False,
        verbose_name="Servidor Passagem Plantão Anterior",
    )
    servidor_recebimento = models.ForeignKey(
        "servidores.Servidor",
        on_delete=models.CASCADE,
        related_name="+",
        null=False,
        blank=False,
        verbose_name="Servidor Recebimento do Plantão",
    )
    ausencias = models.TextField(null=True, blank=True, verbose_name="Ausências")
    patrimonio = models.TextField(null=True, blank=True, verbose_name="Patrimônio")
    expediente = models.TextField(null=True, blank=True, verbose_name="Expediente")
    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")
    informacoes_servidores = models.TextField(null=True, blank=True, verbose_name="Informações dos Servidores")
    outras_informacoes = models.TextField(null=True, blank=True, verbose_name="Outras Informações dos Adolescentes")
    
    instalacoes = models.TextField(
        null=True,
        blank=True,
        verbose_name="Instalações",
    )
    avisos = models.TextField(
        null=True,
        blank=True,
    )
    
    medicacoes = models.TextField(
        null=True,
        blank=True,
        verbose_name="Medicações",
    )
    
    evasoes = models.TextField(
        null=True,
        blank=True,
        verbose_name="Evasões",
    )
    
    vigilancia_noturna = models.TextField(
        null=True,
        blank=True,
        verbose_name="Vigilância Noturna",
    )
    
    alimentacao = models.TextField(
        null=True,
        blank=True,
        verbose_name="Alimentação",
    )
    
    plantonistas = models.ManyToManyField(
        "servidores.Servidor",
        blank=True,
        verbose_name="Plantonistas",
        related_name="plantonistas",
    )

    @property
    def titulo(self):
        if self.de_modulo:
            if self.modulo.unidade.modulos.count() > 1:
                return f"Livro Módulo {self.modulo.descricao} de {self.data_abertura.date().strftime('%d/%m/%Y')}"
            return f"Livro {self.modulo.unidade.sigla} de {self.data_abertura.date().strftime('%d/%m/%Y')}"
        return f"Livro C2 {self.unidade.sigla} de {self.data_abertura.date().strftime('%d/%m/%Y')}"

    def __str__(self):
        dia = self.data_abertura.day
        mes = self.data_abertura.month
        ano = self.data_abertura.year
        if self.de_modulo:
            if self.modulo.unidade.modulos.count()==1:
                return f"Livro {self.modulo.unidade.sigla} de {self.data_abertura.date().strftime('%d/%m/%Y')}"
            return f"Livro Módulo {self.modulo.descricao} {self.modulo.unidade.sigla} de {self.data_abertura.date().strftime('%d/%m/%Y')}"
        if self.de_unidade:
            return f"Livro C2 {self.unidade.sigla} de {self.data_abertura.date().strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ["data_abertura"]
        permissions = (
            (
                "ver_livro_modulos",
                "Pode ver livro de módulos da mesma unidade",
            ),
            (
                "ver_livro_c2",
                "Pode ver livro da mesma unidade (inclui livro C2/GESEG)",
            ),
            (
                "editar_livro_modulos",
                "Pode editar livro de módulos da mesma unidade",
            ),
            (
                "editar_livro_c2",
                "Pode editar livro da mesma unidade (inclui livro C2/GESEG)",
            ),
            (
                "incluir_livro_modulos",
                "Pode incluir livro em módulos da mesma unidade",
            ),
            (
                "incluir_livro_c2",
                "Pode incluir livro na mesma unidade (inclui livro C2/GESEG)",
            ),
            (
                "excluir_livro_modulos",
                "Pode excluir livro em módulos da mesma unidade",
            ),
            (
                "excluir_livro_c2",
                "Pode excluir livro da mesma unidade (inclui entradas em livro C2/GESEG)",
            ),
        )

    @property
    def plantao(self):
        from servidores.models import Plantao
        return Plantao.date_to_plantao(self.data_abertura)
    
    @property
    def numero(self):
        from datetime import datetime
        ano = self.data_abertura.year
        primeiro_de_janeiro = datetime(ano, 1, 1).date()
        return (self.data_abertura.date() - primeiro_de_janeiro).days + 1

    
    @property
    def de_modulo(self):
        return self.modulo is not None

    @property
    def de_unidade(self):
        return self.unidade is not None and self.modulo is None

   
    def clean(self, *args, **kwargs):
        logica_criacao(self)
        logica_livro(self)
        super().clean(*args, **kwargs)

    @property
    def anterior(self):
        if self.anteriores.exists():
            return self.anteriores.order_by('data_abertura').last()
        return None

    @property
    def seguinte(self):
        seguintes =  self.outros_livros.filter(data_abertura__gt=self.data_abertura)
        if seguintes.exists():
            return seguintes.order_by('data_abertura').first()
        return None
    
    @property
    def efetivo_passagem(self):
        if self.seguinte:
            return self.seguinte.efetivo_recebimento
        return None
    
    
    @property
    def outros_livros(self):
        if self.de_modulo:
            qs = Livro._default_manager.filter(modulo=self.modulo)
        else:
            qs = Livro._default_manager.filter(modulo__isnull=True, unidade=self.unidade)
        
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        return qs
    
    @property
    def anteriores(self):
        return self.outros_livros.filter(data_abertura__lt=self.data_abertura)

    @property
    def aberto(self):
        if not self.id:
            return False
        return self.__class__._default_manager.all().last().id == self.id
    
    def copia_efetivo_criacao(self, atividades=True, ausencias=True):
        
        efetivo = EfetivoLivro.objects.create(livro_id = self.id)
        
        if self.de_unidade:
            modulos = self.unidade.modulos.all()
        if self.de_modulo:
            modulos = Modulo.objects.filter(id=self.modulo.id)
        presentes = 0
        ausentes = 0
        for modulo in modulos:
            for quarto in modulo.quartos.all():
                for entrada in quarto.entradas_atuais:
                    if entrada.em_atividade_externa:
                        ausentes+=1
                    else:
                        presentes+=1
                    AdolescenteEfetivoLivro.objects.create(
                        efetivo_id=efetivo.id,
                        adolescente=entrada.adolescente,
                        adolescente_nome=entrada.adolescente.nome,
                        modulo=modulo,
                        modulo_nome=modulo.descricao,
                        quarto=quarto,
                        quarto_nome=str(quarto.numero) if quarto.nome is None else str(quarto.numero) + quarto.nome,
                        atividade = entrada.atividade_atual.atividade if atividades and entrada.em_atividade else None,
                        atividade_nome_curto = entrada.atividade_atual.atividade.nome_curto if atividades and entrada.em_atividade else None,
                        presente = not entrada.em_atividade_externa if ausencias else True
                    )
        
        self.efetivo_recebimento.presentes = presentes
        self.efetivo_recebimento.ausentes = ausentes
        self.efetivo_recebimento.save()
    
    @property
    def chegadas(self):
        from unidades.models import EntradaAdolescente
        unidade = self.modulo.unidade if self.de_modulo else self.unidade
        if self.de_modulo and self.modulo.unidade.modulos.count() > 1:
            qs = EntradaAdolescente.history.filter(modulo = self.modulo, modificado_em__gte = self.data_abertura)
            
            if self.seguinte is not None:
                qs = qs.filter(modificado_em__lt = self.seguinte.data_abertura)
            
            entradas_ids = []
            if self.de_modulo:
                for his in qs:
                    if not (his.prev_record is not None and his.prev_record.modulo == self.modulo):
                        entradas_ids.append(his.id)
            return EntradaAdolescente.objects.filter(id__in=entradas_ids)
        
        qs = EntradaAdolescente.objects.filter(
            unidade = unidade,
            data_entrada__gte=self.data_abertura
        )
        
        if self.seguinte is not None:
            qs = qs.filter(data_entrada__lt = self.seguinte.data_abertura)
        return qs
        
        
        
    @property
    def saidas(self):
        from unidades.models import EntradaAdolescente
        unidade = self.modulo.unidade if self.de_modulo else self.unidade
        if self.de_modulo and self.modulo.unidade.modulos.count() > 1:
            qs = EntradaAdolescente.history.filter(unidade = self.modulo.unidade, modificado_em__gte = self.data_abertura)
            
            if self.seguinte is not None:
                qs = qs.filter(modificado_em__lt = self.seguinte.data_abertura)
            
            entradas_ids = []
            if self.de_modulo:
                for his in qs:
                    if (his.prev_record is not None and his.prev_record.modulo == self.modulo and his.modulo != self.modulo):
                        entradas_ids.append(his.id)
            return EntradaAdolescente.objects.filter(id__in=entradas_ids)
        
        qs = EntradaAdolescente.objects.filter(
            unidade=unidade,
            data_saida__gte=self.data_abertura
        )
        
        if self.seguinte is not None:
            qs = qs.filter(data_saida__lt = self.seguinte.data_abertura)
        return qs
    
    @property
    def atividades_livro(self):
        from atividades.models import HistoricoAtividade
        unidade = self.modulo.unidade if self.de_modulo else self.unidade
        qs = HistoricoAtividade.objects.filter(atividade__unidade = unidade)
        if self.de_modulo:
            qs = qs.filter(modulo = self.modulo)
        
        qs = qs.filter(
            models.Q(data_ida__gte = self.data_abertura) | models.Q(data_retorno__gte = self.data_abertura) 
        )
        
        if self.seguinte is not None:
            qs = qs.filter(
                models.Q(data_ida__lt = self.seguinte.data_abertura) | models.Q(data_retorno__lt = self.seguinte.data_abertura)
            )
            
        return qs.order_by('data_ida')
    
    @property
    def ocorrencias(self):
        from ocorrencias.models import Ocorrencia
        unidade = self.modulo.unidade if self.de_modulo else self.unidade
        if self.de_modulo:
            qs = Ocorrencia.objects.filter(modulo=self.modulo, data_hora__gte = self.data_abertura)
        else:
            ids_modulos = unidade.modulos.values_list('id', flat=True)
            qs = Ocorrencia.objects.filter(modulo__id__in=ids_modulos, data_hora__gte = self.data_abertura)
            
            
        if self.seguinte is not None:
            qs = qs.filter(data_hora__lt = self.seguinte.data_abertura)
            
        return qs
        
class EfetivoLivro(BaseModel):
    presentes = models.IntegerField(null=True, blank=True)
    ausentes = models.IntegerField(null=True, blank=True)
    livro = models.OneToOneField(Livro, on_delete=models.CASCADE, related_name='efetivo_recebimento')
    
    def __str__(self) -> str:
        return f"Efetivo Livro {self.livro}"
    
    class Meta:
        verbose_name = "Efetivo de Abertura de Livro"
        verbose_name = "Efetivos de Abertura de Livros"

class AdolescenteEfetivoLivro(BaseModel):
    efetivo = models.ForeignKey(EfetivoLivro, on_delete=models.CASCADE, null=False, blank=False, related_name='adolescentes')
    adolescente = models.ForeignKey('adolescentes.Adolescente', on_delete=models.DO_NOTHING, null=True, blank=True)
    adolescente_nome = models.CharField(max_length=150, null=True, blank=True)
    modulo = models.ForeignKey('unidades.Modulo', on_delete=models.DO_NOTHING, null=True, blank=True)
    modulo_nome = models.CharField(max_length=64, null=True, blank=True)
    quarto = models.ForeignKey('unidades.Quarto', on_delete=models.DO_NOTHING, null=True, blank=True)
    quarto_nome = models.CharField(max_length=64, null=True, blank=True)
    atividade = models.ForeignKey('atividades.Atividade', on_delete=models.DO_NOTHING, null=True, blank=True)
    atividade_nome_curto = models.CharField(max_length=20, null=True, blank=True)
    presente = models.BooleanField()


class Acompanhamento(BaseModel):
    livro = models.ForeignKey(
        "Livro",
        on_delete=models.CASCADE,
        related_name="acompanhamentos"
    )
    data_hora = models.DateTimeField(null=False, blank=False)
    descricao = models.TextField(
        null=True,
        blank=False,
        verbose_name="Descrição",
    )

    def __str__(self):
        return f"Acompanhamento {self.id}"

    def clean(self):
        super().clean()
        if self.data_hora is not None:
            if self.data_hora < self.livro.data_abertura:
                from django.core.exceptions import ValidationError
                raise ValidationError({'data_hora':'Data deve ser posterior à abertura do Livro'})

    class Meta:
        ordering=["data_hora"]
        verbose_name_plural = "Acompanhamentos"
        verbose_name = "Acompanhamento"
