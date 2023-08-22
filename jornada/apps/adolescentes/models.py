from core.models import BaseModel
from core.models.utils import generate_uuid4_filename
from core.validators import (
    CaracteresEspeciaisValidator, 
    SomenteNumeros,
    cidade_do_uf, 
    valida, 
    validate_file_size
)
from django.db import models
from dominios.models import Bairro, Cidade, Cor, Genero, Uf

from .logic import logica_principal, logica_adolescente


class Adolescente(BaseModel):
    """
    Modelo que contém dos dados de adolescentes.
    """
    somente_numeros_validator = SomenteNumeros()
    caracter_especial_validator = CaracteresEspeciaisValidator()

    sipia = models.CharField(
        "SIPIA",
        max_length=6,
        blank=True,
        null=True,
        validators=[somente_numeros_validator],
        unique=True,
        db_index=True,
    )
    id_jornada = models.CharField(
        "ID_JORNADA",
        max_length=6,
        blank=False,
        null=False,
        validators=[somente_numeros_validator],
        unique=True,
        editable=False,
        db_index=True,
    )
    
    def natural_key(self):
        return (self.id_jornada)
    
    nome = models.CharField("Nome", max_length=100, blank=False, null=False, validators=[caracter_especial_validator])
    possui_homonimo = models.BooleanField(default=False)
    checa_homonimo = models.BooleanField(default=True)
    nome_social = models.CharField("Nome Social", max_length=100, blank=True, null=True)
    data_nascimento = models.DateField("Data de Nascimento", blank=False, null=True)
    data_falecimento = models.DateField("Data de Falecimento", blank=True, null=True)
    apelido = models.CharField("Apelido", max_length=50, blank=True, null=True)
    nome_mae = models.CharField("Nome da Mãe", max_length=50, blank=True, null=True)
    genero = models.ForeignKey(
        Genero, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Gênero"
    )
    cor = models.ForeignKey(
        Cor, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Cor"
    )
    email = models.EmailField(max_length=254, blank=True, null=True)
    data_registro = models.DateTimeField(
        "Data de Registro", auto_now_add=True, blank=True, null=True
    )

    # Documentação Pessoal
    rg = models.CharField(
        "RG",
        max_length=7,
        blank=True,
        null=True,
        validators=[somente_numeros_validator],
    )
    orgao_expedidor = models.CharField(
        "Órgão Expedidor", max_length=20, blank=True, null=True
    )
    uf_expedicao = models.ForeignKey(
        "dominios.Uf",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="UF Expedição",
    )
    cpf = models.CharField(
        "CPF",
        max_length=11,
        blank=True,
        null=True,
        unique=True,
        validators=[somente_numeros_validator],
    )
    cnh = models.CharField(
        "CNH",
        max_length=30,
        blank=True,
        null=True,
        unique=True,
    )
    ctps = models.CharField("CTPS", max_length=30, blank=True, null=True)
    pis = models.CharField("PIS", max_length=30, blank=True, null=True)
    titulo_eleitor = models.CharField(
        "Título de Eleitor", max_length=30, blank=True, null=True
    )
    e_gov = models.CharField(verbose_name="E-Gov", max_length=200, blank=True, null=True)
    cam = models.CharField(verbose_name="CAM",  max_length=100, blank=True, null=True)
    cdi = models.CharField(verbose_name="CDI",  max_length=100, blank=True, null=True)
    outros_documentos = models.CharField(
        "Outros Documentos", max_length=100, blank=True, null=True
    )
    data_expedicao_identidade = models.CharField(
        "Data de expedição da identidade", max_length=30, blank=True, null=True
    )
    naturalidade = models.CharField(
        "Naturalidade", max_length=150, blank=True, null=True
    )
    nacionalidade = models.CharField(
        "Nacionalidade", max_length=100, blank=True, null=True
    )
    certidao_nascimento = models.CharField(
        "Certidão de Nascimento", max_length=150, blank=True, null=True
    )
    cartao_bancario = models.CharField(
        "Cartão Bancário", max_length=100, blank=True, null=True
    )

    class Meta:
        ordering = ["nome"]
        permissions = (
            ("ver_todos", "Pode ver todos os adolescentes do Sistema"),
            ("ver_da_unidade", "Pode ver adolescentes lotados na mesma unidade"),
            ("editar_todos", "Pode editar todos os adolescentes do Sistema"),
            ("editar_da_unidade", "Pode editar adolescentes lotados na mesma unidade"),
            ("incluir", "Pode incluir adolescentes"),
        )

    def __str__(self):
        return f"{self.nome}"

    @property
    def foto_mais_recente(self):
        return self.fotos.last()

    @property
    def telefones_autorizados(self):
        return self.telefones.filter(autorizado=True).all()

    @property
    def todas_fotos(self):
        return self.fotos.all()

    @property
    def processos_ativos(self):
        return self.processos.filter(ativo=True)

    @property
    def possui_entrada_ativa(self):
        return self.entradas_ativas.exists()
    
    @property
    def unidade_atual(self):
        return self.entrada_em_unidade_atual.unidade

    @property
    def entradas_ativas(self):
        return self.entradas_em_unidades.exclude(status=4)

    @property
    def entrada_em_unidade_atual(self):
        if self.entradas_ativas.exists():
            if self.entradas_ativas.count() == 1:
                return self.entradas_ativas.first()
            else:
                return self.entradas_ativas.filter(lotado=True).first()
            
        return None
        
                
    @property
    def tem_entrada_pendente(self):
        return self.entradas_em_unidades.filter(status=1).exists()

    @property
    def unidade_entrada_pendente(self):
        return self.entradas_em_unidades.filter(status=1).first().unidade

    @property
    def tem_saida_pendente(self):
        return self.entradas_em_unidades.filter(status=3).exists()

    @property
    def unidade_saida_pendente(self):
        return self.entradas_em_unidades.filter(status=3).first().unidade

    @property
    def atendimento_educacao_atual(self):
        return self.atendimento_educacao.last()

    @property
    def endereco_atual(self):
        return self.enderecos.filter(reside=True).first()

    @property
    def tem_risco_ativo(self):
        return self.riscos.filter(ativo=True).exists()
    
    @property
    def riscos_ativos(self):
        return self.riscos.filter(ativo=True)
    

    @property
    def familiares_autorizados_visita(self):
        return self.familiares.filter(visitante_autorizado=True)
    
    @classmethod
    def vinculados_em_unidade(cls):
        from unidades.models import EntradaAdolescente
        return cls.objects.filter(id__in=EntradaAdolescente.objects.exclude(status=4).values_list('adolescente__id', flat=True))

    @classmethod
    def nao_vinculados_em_unidade(cls):
        from unidades.models import EntradaAdolescente
        return cls.objects.exclude(id__in=EntradaAdolescente.objects.exclude(status=4).values_list('adolescente__id', flat=True))

    def clean(self, *args, **kwargs):
        logica_adolescente(self)
        super().clean(*args, **kwargs)

class DocumentoAnexo(BaseModel):
    adolescente = models.ForeignKey(
        Adolescente, on_delete=models.CASCADE, related_name="documentos_anexados"
    )
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField("Descrição", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.descricao}"


class Familiar(BaseModel):
    caracter_especial_validator = CaracteresEspeciaisValidator()
    somente_numeros_validator = SomenteNumeros()

    adolescente = models.ForeignKey(
        Adolescente, on_delete=models.CASCADE, related_name="familiares"
    )
    nome = models.CharField(
        "Nome do Familiar", max_length=100, validators=[caracter_especial_validator]
    )
    observacoes = models.TextField(
        "Observações", max_length=1000, blank=True, null=True
    )
    vinculo = models.ForeignKey(
        "dominios.VinculoFamiliar",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Vínculo Familiar",
    )
    cpf = models.CharField(
        "CPF",
        max_length=11,
        blank=True,
        null=True,
        validators=[somente_numeros_validator],
    )
    rg = models.CharField(
        "RG",
        max_length=11,
        blank=True,
        null=True,
        validators=[somente_numeros_validator],
    )
    orgao_emissor = models.CharField(
        "Órgão Emissor",
        max_length=50,
        blank=True,
        null=True
    )
    trabalho = models.CharField(
        "Trabalho",
        max_length=50,
        blank=True,
        null=True,
        validators=[caracter_especial_validator],
    )
    renda = models.CharField(
        "Renda",
        max_length=50,
        blank=True,
        null=True
    )
    
    responsavel = models.BooleanField("É Responsável", default=False)

    visitante_autorizado = models.BooleanField("Visitante autorizado", default=False)

    def __str__(self):
        return f"{self.nome} ({self.vinculo})"


class Foto(BaseModel):
    """
    Modelo com as fotos dos adolescentes.
    Permite inserir descrição e indicar se é a foto principal.
    """

    adolescente = models.ForeignKey(
        Adolescente, on_delete=models.CASCADE, related_name="fotos"
    )
    foto = models.ImageField(
        upload_to=generate_uuid4_filename,
        verbose_name="Foto",
        validators=[validate_file_size],
    )
    principal = models.BooleanField("É Principal", default=False)
    descricao = models.CharField("Descrição", max_length=255, blank=True, null=True)

    def clean(self, *args, **kwargs):
        logica_principal(self)
        super().clean(*args, **kwargs)


class Observacao(BaseModel):
    """
    Modelo das observações dos adolescentes feito pelos agentes.
    Permite inserir todas as observações feitas pelos agenstes
    durante cada plantão.
    """

    adolescente = models.ForeignKey(
        Adolescente, on_delete=models.CASCADE, related_name="observacoes"
    )
    observacao = models.TextField("Descrição", max_length=1000, blank=True, null=True)

    def clean(self, *args, **kwargs):
        logica_principal(self)
        super().clean(*args, **kwargs)


class Telefone(BaseModel):
    """
    Modelo com os telefones dos adolescentes.
    Permite inserir descrição e indicar se é o telefone principal.
    O validador garante_unico_principal assegura que se o adolescentes
    já tinha um telefone principal, o principal anterior terá essa opção desmarcada.
    """

    adolescente = models.ForeignKey(
        Adolescente, on_delete=models.CASCADE, related_name="telefones"
    )
    telefone = models.CharField("Número de Telefone", max_length=20)
    descricao = models.CharField("Descrição", max_length=100, blank=True, null=True)
    autorizado = models.BooleanField("Telefone Autorizado", default=False)

    def __str__(self):
        return f"{self.telefone} - {self.descricao}"

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)



class Relatorio(BaseModel):
    adolescente = models.ForeignKey(
        Adolescente, 
        on_delete=models.CASCADE, 
        related_name="relatorios",
    )
    descricao = models.CharField("Descrição", max_length=100, blank=True, null=True)
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    
    def __str__(self):
        return f"Relatorio: {self.descricao} de {self.adolescente}"



class Endereco(BaseModel):
    """
    Modelo com os endereços dos adolescentes.
    Permite inserir descrição e indicar se é o endereço principal.
    O validador garante_unico_principal assegura que se o adolescentes
    já tinha um endereço principal, o principal anterior terá essa opção desmarcada.
    """

    adolescente = models.ForeignKey(
        Adolescente,
        on_delete=models.CASCADE,
        related_name="enderecos",
    )
    uf = models.ForeignKey(Uf, on_delete=models.SET_NULL, null=True, verbose_name="UF")
    cidade = models.ForeignKey(
        Cidade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Cidade"
    )
    bairro = models.ForeignKey(
        Bairro, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Bairro"
    )
    reside = models.BooleanField("Reside Atualmente", default=False)
    descricao = models.CharField("Descrição", max_length=255, blank=True, null=True)
    cep = models.CharField("CEP", max_length=10, blank=True, null=True)
    logradouro = models.CharField("Logradouro", max_length=255, blank=True, null=True)
    complemento = models.CharField("Complemento", max_length=255, blank=True, null=True)
    numero = models.CharField("Número", max_length=50, blank=True, null=True)

    def __str__(self):
        return ""

    def clean(self, *args, **kwargs):
        if self.updating:
            residencia_anterior = self.__class__._default_manager.filter(
                ~models.Q(id=self.id),  # pra nao trazer o mesmo self
                adolescente=self.adolescente,
                reside=True,
            )

            if self.reside and residencia_anterior.exists():
                if self != residencia_anterior:
                    residencia_anterior.update(reside=False)

        super().clean(*args, **kwargs)

class AnexoFamiliar(BaseModel):
    familiar = models.ForeignKey(
        Familiar,
        models.CASCADE,
        related_name="anexos",
    )
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Descrição",
    )

class AnexoEndereco(BaseModel):
    endereco = models.ForeignKey(
        Endereco,
        models.CASCADE,
        related_name="anexos",
    )
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Descrição",
    )

class AnexoTelefone(BaseModel):
    telefone = models.ForeignKey(
        Telefone,
        models.CASCADE,
        related_name="anexos",
    )
    anexo = models.FileField(max_length=500, upload_to=generate_uuid4_filename, validators=[validate_file_size])
    descricao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Descrição",
    )


