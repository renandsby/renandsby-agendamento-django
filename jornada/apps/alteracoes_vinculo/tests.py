from django.test import TestCase
from solicitacoes.models import Solicitacao
from dominios.models import TipoVagaUnidade, TipoEntradaUnidade, TipoSaidaUnidade
from alteracoes_vinculo.models import Vinculacao, Transferencia, Desvinculacao
from adolescentes.models import Adolescente
from processos.models import Processo
from unidades.models import Unidade, EntradaAdolescente
from django.core.exceptions import ValidationError
import datetime

class AltVinculoTestCase(TestCase):
    fixtures = [
        'fixtures/base/1-dominios.json', 
        'fixtures/base/4-base_unidades.json',
    ]

    @classmethod
    def setUpTestData(cls):
        ''' Isso aqui roda uma vez só antes de todos os testes '''
        cls.UNIRE = Unidade.objects.get(sigla='UNIRE')
        cls.GERSEMIMET = Unidade.objects.get(sigla='GERSEMIMET')
        cls.GEAMANB = Unidade.objects.get(sigla='GEAMANB')
        
        

    
    def setUp(self):
        ''' Isso aqui roda antes de cada teste '''
        self.AD_NAO_LOTADO = Adolescente.objects.create(nome="ADOLESCENTE SEM UNIDADE", data_nascimento=datetime.datetime.now(), cor_id=1, genero_id=1)
        Processo.objects.create(adolescente = self.AD_NAO_LOTADO, numero = "1234516" )
        self.AD_LOTADO_UNIRE = Adolescente.objects.create(nome="ADOLESCENTE LOTADO UNIRE", data_nascimento=datetime.datetime.now(), cor_id=1, genero_id=1)
        EntradaAdolescente.objects.create(
            adolescente = self.AD_LOTADO_UNIRE,
            processo = Processo.objects.create(adolescente = self.AD_LOTADO_UNIRE, numero = "123456" ), 
            unidade = self.UNIRE, 
            status = EntradaAdolescente.Status.ENTRADA_REALIZADA,
            modulo = self.UNIRE.modulos.first(),
            quarto = self.UNIRE.modulos.first().quartos.first()
        )
        
        self.AD_LOTADO_GEAMANB = Adolescente.objects.create(nome="ADOLESCENTE LOTADO GEAMANB", data_nascimento=datetime.datetime.now(), cor_id=1, genero_id=1)
        EntradaAdolescente.objects.create(
            adolescente = self.AD_LOTADO_GEAMANB,
            processo = Processo.objects.create(adolescente = self.AD_LOTADO_GEAMANB, numero = "123456" ), 
            unidade = self.GEAMANB, 
            status = EntradaAdolescente.Status.ENTRADA_REALIZADA
        )

        self.AD_SAIDA_PENDENTE_UNIRE = Adolescente.objects.create(nome="ADOLESCENTE COM SAIDA PENDENTE UNIRE", data_nascimento=datetime.datetime.now(), cor_id=1, genero_id=1)
        EntradaAdolescente.objects.create(
            adolescente = self.AD_SAIDA_PENDENTE_UNIRE,
            processo = Processo.objects.create(adolescente = self.AD_SAIDA_PENDENTE_UNIRE, numero = "123456"),
            unidade = self.UNIRE, 
            status = EntradaAdolescente.Status.SAIDA_PENDENTE,
            modulo = self.UNIRE.modulos.first(),
            quarto = self.UNIRE.modulos.first().quartos.first()
        )

        self.AD_ENTRADA_PENDENTE_UNIRE = Adolescente.objects.create(nome="ADOLESCENTE COM ENTRADA PENDENTE UNIRE", data_nascimento=datetime.datetime.now(), cor_id=1, genero_id=1)
        EntradaAdolescente.objects.create(
            adolescente = self.AD_ENTRADA_PENDENTE_UNIRE,
            processo = Processo.objects.create(adolescente = self.AD_ENTRADA_PENDENTE_UNIRE, numero = "123456" ),
            unidade = self.UNIRE, 
            status = EntradaAdolescente.Status.ENTRADA_PENDENTE
        )

    def test_setup(self):
         self.assertEqual(self.AD_LOTADO_UNIRE.entrada_em_unidade_atual.status, EntradaAdolescente.Status.ENTRADA_REALIZADA)
         self.assertEqual(self.AD_SAIDA_PENDENTE_UNIRE.entrada_em_unidade_atual.status, EntradaAdolescente.Status.SAIDA_PENDENTE)
         self.assertEqual(self.AD_ENTRADA_PENDENTE_UNIRE.entrada_em_unidade_atual.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
    
    
    #############################
    #                           #
    #        VINCULAÇÃO         #
    #                           #
    #############################
    
    # Começa com status pendente
    def test_vinculacao_comeca_pendente(self):
        vinc = Vinculacao(
            adolescente = self.AD_LOTADO_UNIRE
        )
        self.assertEqual(vinc.status, Vinculacao.Status.PENDENTE)
        vinc.save()
        self.assertEqual(vinc.status, Vinculacao.Status.PENDENTE)
        
    # não permite processo que não seja do adolescente selecionado
    def test_vinculacao_nao_permite_processo_de_adol_diferente(self):
        with self.assertRaises(ValidationError):
            vinc = Vinculacao.objects.create(
                adolescente = Adolescente.objects.create(
                    nome="ADOLESCENTE VINCULADO UNIRE", 
                    data_nascimento=datetime.datetime.now(), 
                    cor_id=1, 
                    genero_id=1
                ),    
                processo = self.AD_LOTADO_UNIRE.processos.first()
            )
        with self.assertRaises(ValidationError):
            vinc = Vinculacao(
                adolescente = Adolescente.objects.create(
                    nome="ADOLESCENTE VINCULADO UNIRE", 
                    data_nascimento=datetime.datetime.now(), 
                    cor_id=1, 
                    genero_id=1
                ),    
                processo = self.AD_LOTADO_UNIRE.processos.first()
            )
            vinc.save()
    
    def test_vincular_adolescente_sem_lotacao(self):
        vinc = Vinculacao.objects.create(
            adolescente = self.AD_NAO_LOTADO,
        )
        
        # Exige Unidade Destino
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.unidade_destino = self.UNIRE
        
        # Exige tipo de vaga
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.tipo_vaga = TipoVagaUnidade.objects.first()
        
        # Exige data de entrada
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.data_entrada = datetime.datetime.now()
        
        # Exige tipo de de entrada
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.tipo_entrada = TipoEntradaUnidade.objects.first()
        
        try:
            vinc.vincular()    
        except:
            self.fail("vinc.vincular() levantou uma Exception!")
        
        self.assertTrue(self.AD_NAO_LOTADO.possui_entrada_ativa)
        self.assertEqual(self.AD_NAO_LOTADO.unidade_atual, self.UNIRE)
        self.assertEqual(self.AD_NAO_LOTADO.entrada_em_unidade_atual.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
        
    
    def test_vincular_adolescente_com_lotacao(self):
        vinc = Vinculacao.objects.create(
            adolescente = self.AD_LOTADO_UNIRE,
        )
        # Exige Data de saída
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.data_saida = datetime.datetime.now()
        
        # Exige tipo de saida
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.tipo_saida = TipoSaidaUnidade.objects.first()
        
        # Exige Unidade Destino
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.unidade_destino = self.GERSEMIMET
        
        # Exige tipo de vaga
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.tipo_vaga = TipoVagaUnidade.objects.first()
        
        # Exige data de entrada
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.data_entrada = datetime.datetime.now()
        
        # Exige tipo de de entrada
        with self.assertRaises(ValidationError):
            vinc.vincular()
        
        vinc.tipo_entrada = TipoEntradaUnidade.objects.first()
        
        try:
            vinc.vincular()    
        except:
            self.fail("vinc.vincular() levantou uma Exception!")
        
        self.assertEqual(vinc.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_PENDENTE)
        self.assertTrue(self.AD_LOTADO_UNIRE.possui_entrada_ativa)
        self.assertEqual(self.AD_LOTADO_UNIRE.unidade_atual, self.UNIRE)
        self.assertEqual(self.AD_LOTADO_UNIRE.entrada_em_unidade_atual, vinc.entrada_antiga)
        self.assertEqual(self.AD_LOTADO_UNIRE.entradas_ativas.count(), 2)
        entrada_nova = self.AD_LOTADO_UNIRE.entradas_ativas.filter(status=1).first()
        self.assertEqual(entrada_nova.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
        self.assertEqual(entrada_nova.unidade, self.GERSEMIMET)
            
        
    
    def test_vincular_adolescente_com_saida_pendente(self):
        vinc = Vinculacao.objects.create(
            adolescente = self.AD_SAIDA_PENDENTE_UNIRE,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
            unidade_destino = self.GERSEMIMET,
            tipo_vaga = TipoVagaUnidade.objects.first(),
            data_entrada = datetime.datetime.now(),
            tipo_entrada = TipoEntradaUnidade.objects.first()
        )
        
        try:
            vinc.vincular()    
        except:
            self.fail("vinc.vincular() levantou uma Exception!")
        
        self.assertEqual(vinc.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_PENDENTE)
        self.assertTrue(self.AD_SAIDA_PENDENTE_UNIRE.possui_entrada_ativa)
        self.assertEqual(self.AD_SAIDA_PENDENTE_UNIRE.unidade_atual, self.UNIRE)
        self.assertEqual(self.AD_SAIDA_PENDENTE_UNIRE.entrada_em_unidade_atual, vinc.entrada_antiga)
        entrada_nova = self.AD_SAIDA_PENDENTE_UNIRE.entradas_ativas.filter(status=1).first()
        self.assertEqual(entrada_nova.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
        self.assertEqual(entrada_nova.unidade, self.GERSEMIMET)
    
    
    def test_vincular_adolescente_com_entrada_pendente(self):
        vinc = Vinculacao.objects.create(
            adolescente = self.AD_ENTRADA_PENDENTE_UNIRE,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
            unidade_destino = self.GERSEMIMET,
            tipo_vaga = TipoVagaUnidade.objects.first(),
            data_entrada = datetime.datetime.now(),
            tipo_entrada = TipoEntradaUnidade.objects.first()
        )
        
        try:
            vinc.vincular()    
        except:
            self.fail("vinc.vincular() levantou uma Exception!")
        
        self.assertEqual(vinc.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_REALIZADA)
        self.assertTrue(self.AD_ENTRADA_PENDENTE_UNIRE.possui_entrada_ativa)
        self.assertEqual(self.AD_ENTRADA_PENDENTE_UNIRE.unidade_atual, self.GERSEMIMET)
        self.assertEqual(self.AD_ENTRADA_PENDENTE_UNIRE.entrada_em_unidade_atual, vinc.entrada_criada)
        self.assertEqual(self.AD_ENTRADA_PENDENTE_UNIRE.entrada_em_unidade_atual.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
    
    def test_vincular_adolescente_com_entrada_e_saida_pendente(self):
        ad = Adolescente.objects.create(
            nome="ADOLESCENTE VINCULADO UNIRE", 
            data_nascimento=datetime.datetime.now(), 
            cor_id=1, 
            genero_id=1
        )
        
        ent_pend = EntradaAdolescente.objects.create(
            adolescente = ad,
            processo = Processo.objects.create(adolescente = ad, numero = "123456" ), 
            unidade = self.GERSEMIMET, 
            status = EntradaAdolescente.Status.ENTRADA_PENDENTE,
        )
        
        sai_pend = EntradaAdolescente.objects.create(
            adolescente = ad,
            processo = Processo.objects.create(adolescente = ad, numero = "123456" ), 
            unidade = self.UNIRE, 
            status = EntradaAdolescente.Status.SAIDA_PENDENTE,
            modulo = self.UNIRE.modulos.first(),
            quarto = self.UNIRE.modulos.first().quartos.first()
        )
        
        vinc = Vinculacao.objects.create(
            adolescente = ad,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
            unidade_destino = self.GEAMANB,
            tipo_vaga = TipoVagaUnidade.objects.first(),
            data_entrada = datetime.datetime.now(),
            tipo_entrada = TipoEntradaUnidade.objects.first()
        )
        
        
        try:
            vinc.vincular()    
        except:
            self.fail("vinc.vincular() levantou uma Exception!")  
        
        self.assertEqual(EntradaAdolescente.objects.get(pk=ent_pend.pk).status, EntradaAdolescente.Status.SAIDA_REALIZADA)
        self.assertEqual(EntradaAdolescente.objects.get(pk=sai_pend.pk).status, EntradaAdolescente.Status.SAIDA_PENDENTE)
        self.assertEqual(vinc.entrada_antiga, sai_pend)
        self.assertTrue(ad.possui_entrada_ativa)
        self.assertEqual(ad.unidade_atual, self.UNIRE)
        self.assertEqual(ad.entradas_ativas.count(), 2)
        entrada_nova = ad.entradas_ativas.filter(status=1).first()
        self.assertEqual(entrada_nova.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
        self.assertEqual(entrada_nova.unidade, self.GEAMANB)
        
    
    def test_vincular_adolescente_lotado_em_geama(self):
        vinc = Vinculacao.objects.create(
            adolescente = self.AD_LOTADO_GEAMANB,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
            unidade_destino = self.GERSEMIMET,
            tipo_vaga = TipoVagaUnidade.objects.first(),
            data_entrada = datetime.datetime.now(),
            tipo_entrada = TipoEntradaUnidade.objects.first()
        )
        
        try:
            vinc.vincular()    
        except:
            self.fail("vinc.vincular() levantou uma Exception!")
        
        self.assertEqual(vinc.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_REALIZADA)
        self.assertTrue(self.AD_LOTADO_GEAMANB.possui_entrada_ativa)
        self.assertEqual(self.AD_LOTADO_GEAMANB.unidade_atual, self.GERSEMIMET)
        self.assertEqual(self.AD_LOTADO_GEAMANB.entrada_em_unidade_atual, vinc.entrada_criada)
        self.assertEqual(self.AD_LOTADO_GEAMANB.entrada_em_unidade_atual.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
        
        
    
    
    #############################
    #                           #
    #       TRANSFERÊNCIA       #
    #                           #
    #############################
    
    # Começa com status pendente
    def test_transferencia_comeca_pendente(self):
        transf = Transferencia(
            adolescente = self.AD_LOTADO_UNIRE
        )
        self.assertEqual(transf.status, Transferencia.Status.PENDENTE)
        transf.save()
        self.assertEqual(transf.status, Transferencia.Status.PENDENTE)
        
    # não permite processo que não seja do adolescente selecionado
    def test_transferencia_nao_permite_processo_de_adol_diferente(self):
        with self.assertRaises(ValidationError):
            transf = Transferencia.objects.create(
                adolescente = Adolescente.objects.create(
                    nome="ADOLESCENTE VINCULADO UNIRE", 
                    data_nascimento=datetime.datetime.now(), 
                    cor_id=1, 
                    genero_id=1
                ),    
                processo = self.AD_LOTADO_UNIRE.processos.first()
            )
        with self.assertRaises(ValidationError):
            transf = Transferencia(
                adolescente = Adolescente.objects.create(
                    nome="ADOLESCENTE VINCULADO UNIRE", 
                    data_nascimento=datetime.datetime.now(), 
                    cor_id=1, 
                    genero_id=1
                ),    
                processo = self.AD_LOTADO_UNIRE.processos.first()
            )
            transf.save()
    
    def test_transferir_adolescente_sem_lotacao(self):
        transf = Transferencia.objects.create(
            adolescente = self.AD_NAO_LOTADO,
        )
        
        # Exige Unidade Destino
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.unidade_destino = self.UNIRE
        
        # Exige tipo de vaga
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.tipo_vaga = TipoVagaUnidade.objects.first()
        
        # Exige data de entrada
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.data_entrada = datetime.datetime.now()
        
        # Exige tipo de de entrada
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.tipo_entrada = TipoEntradaUnidade.objects.first()
        
        try:
            transf.transferir()    
        except:
            self.fail("transf.transferir() levantou uma Exception!")
        
        self.assertTrue(self.AD_NAO_LOTADO.possui_entrada_ativa)
        self.assertEqual(self.AD_NAO_LOTADO.unidade_atual, self.UNIRE)
        self.assertEqual(self.AD_NAO_LOTADO.entrada_em_unidade_atual.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
        
    
    def test_transferir_adolescente_com_lotacao(self):
        transf = Transferencia.objects.create(
            adolescente = self.AD_LOTADO_UNIRE,
        )
        # Exige Data de saída
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.data_saida = datetime.datetime.now()
        
        # Exige tipo de saida
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.tipo_saida = TipoSaidaUnidade.objects.first()
        
        # Exige Unidade Destino
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.unidade_destino = self.GERSEMIMET
        
        # Exige tipo de vaga
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.tipo_vaga = TipoVagaUnidade.objects.first()
        
        # Exige data de entrada
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.data_entrada = datetime.datetime.now()
        
        # Exige tipo de de entrada
        with self.assertRaises(ValidationError):
            transf.transferir()
        
        transf.tipo_entrada = TipoEntradaUnidade.objects.first()
        
        try:
            transf.transferir()    
        except:
            self.fail("transf.transferir() levantou uma Exception!")
        
        self.assertEqual(transf.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_PENDENTE)
        self.assertTrue(self.AD_LOTADO_UNIRE.possui_entrada_ativa)
        self.assertEqual(self.AD_LOTADO_UNIRE.unidade_atual, self.UNIRE)
        self.assertEqual(self.AD_LOTADO_UNIRE.entrada_em_unidade_atual, transf.entrada_antiga)
        self.assertEqual(self.AD_LOTADO_UNIRE.entradas_ativas.count(), 2)
        entrada_nova = self.AD_LOTADO_UNIRE.entradas_ativas.filter(status=1).first()
        self.assertEqual(entrada_nova.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
        self.assertEqual(entrada_nova.unidade, self.GERSEMIMET)
    
    def test_transferir_adolescente_com_saida_pendente(self):
        transf = Transferencia.objects.create(
            adolescente = self.AD_SAIDA_PENDENTE_UNIRE,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
            unidade_destino = self.GERSEMIMET,
            tipo_vaga = TipoVagaUnidade.objects.first(),
            data_entrada = datetime.datetime.now(),
            tipo_entrada = TipoEntradaUnidade.objects.first()
        )
        
        try:
            transf.transferir()    
        except:
            self.fail("transf.transferir() levantou uma Exception!")
        
        self.assertEqual(transf.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_PENDENTE)
        self.assertTrue(self.AD_SAIDA_PENDENTE_UNIRE.possui_entrada_ativa)
        self.assertEqual(self.AD_SAIDA_PENDENTE_UNIRE.unidade_atual, self.UNIRE)
        self.assertEqual(self.AD_SAIDA_PENDENTE_UNIRE.entrada_em_unidade_atual, transf.entrada_antiga)
        self.assertEqual(self.AD_SAIDA_PENDENTE_UNIRE.entradas_ativas.count(), 2)
        entrada_nova = self.AD_SAIDA_PENDENTE_UNIRE.entradas_ativas.filter(status=1).first()
        self.assertEqual(entrada_nova.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
        self.assertEqual(entrada_nova.unidade, self.GERSEMIMET)
    
    
    def test_transferir_adolescente_com_entrada_pendente(self):
        transf = Transferencia.objects.create(
            adolescente = self.AD_ENTRADA_PENDENTE_UNIRE,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
            unidade_destino = self.GERSEMIMET,
            tipo_vaga = TipoVagaUnidade.objects.first(),
            data_entrada = datetime.datetime.now(),
            tipo_entrada = TipoEntradaUnidade.objects.first()
        )
        
        try:
            transf.transferir()    
        except:
            self.fail("transf.transferir() levantou uma Exception!")
        
        self.assertEqual(transf.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_REALIZADA)
        self.assertTrue(self.AD_ENTRADA_PENDENTE_UNIRE.possui_entrada_ativa)
        self.assertEqual(self.AD_ENTRADA_PENDENTE_UNIRE.unidade_atual, self.GERSEMIMET)
        self.assertEqual(self.AD_ENTRADA_PENDENTE_UNIRE.entrada_em_unidade_atual, transf.entrada_criada)
        self.assertEqual(self.AD_ENTRADA_PENDENTE_UNIRE.entrada_em_unidade_atual.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
    
    
    def test_transferir_adolescente_lotado_em_geama(self):
        transf = Transferencia.objects.create(
            adolescente = self.AD_LOTADO_GEAMANB,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
            unidade_destino = self.GERSEMIMET,
            tipo_vaga = TipoVagaUnidade.objects.first(),
            data_entrada = datetime.datetime.now(),
            tipo_entrada = TipoEntradaUnidade.objects.first()
        )
        
        try:
            transf.transferir()    
        except:
            self.fail("transf.transferir() levantou uma Exception!")
        
        self.assertEqual(transf.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_REALIZADA)
        self.assertTrue(self.AD_LOTADO_GEAMANB.possui_entrada_ativa)
        self.assertEqual(self.AD_LOTADO_GEAMANB.unidade_atual, self.GERSEMIMET)
        self.assertEqual(self.AD_LOTADO_GEAMANB.entrada_em_unidade_atual, transf.entrada_criada)
        self.assertEqual(self.AD_LOTADO_GEAMANB.entrada_em_unidade_atual.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
    
    
    #############################
    #                           #
    #       DESVINCULAÇÃO       #
    #                           #
    #############################
    
    # Começa com status pendente
    def test_desvinculacao_comeca_pendente(self):
        desv = Desvinculacao(
            adolescente = self.AD_LOTADO_UNIRE
        )
        self.assertEqual(desv.status, Desvinculacao.Status.PENDENTE)
        desv.save()
        self.assertEqual(desv.status, Desvinculacao.Status.PENDENTE)
        
    # não permite processo que não seja do adolescente selecionado
    def test_desvinculacao_nao_permite_processo_de_adol_diferente(self):
        with self.assertRaises(ValidationError):
            desv = Desvinculacao.objects.create(
                adolescente = Adolescente.objects.create(
                    nome="ADOLESCENTE VINCULADO UNIRE", 
                    data_nascimento=datetime.datetime.now(), 
                    cor_id=1, 
                    genero_id=1
                ),    
                processo = self.AD_LOTADO_UNIRE.processos.first()
            )
        with self.assertRaises(ValidationError):
            desv = Desvinculacao(
                adolescente = Adolescente.objects.create(
                    nome="ADOLESCENTE VINCULADO UNIRE", 
                    data_nascimento=datetime.datetime.now(), 
                    cor_id=1, 
                    genero_id=1
                ),    
                processo = self.AD_LOTADO_UNIRE.processos.first()
            )
            desv.save()
    
    def test_desvincular_adolescente_sem_lotacao(self):
        desv = Desvinculacao.objects.create(
            adolescente = self.AD_NAO_LOTADO,
        )
        
        try:
            desv.desvincular()    
        except:
            self.fail("desv.desvincular() levantou uma Exception!")
        
        self.assertFalse(self.AD_NAO_LOTADO.possui_entrada_ativa)
    
    def test_desvincular_adolescente_com_lotacao(self):
        desv = Desvinculacao.objects.create(
            adolescente = self.AD_LOTADO_UNIRE,
        )
        # Exige Data de saída
        with self.assertRaises(ValidationError):
            desv.desvincular()
        
        desv.data_saida = datetime.datetime.now()
        
        # Exige tipo de saida
        with self.assertRaises(ValidationError):
            desv.desvincular()
        
        desv.tipo_saida = TipoSaidaUnidade.objects.first()
        
        try:
            desv.desvincular()    
        except:
            self.fail("desv.desvincular() levantou uma Exception!")
        
        self.assertEqual(desv.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_PENDENTE)
        self.assertEqual(self.AD_LOTADO_UNIRE.entrada_em_unidade_atual, desv.entrada_antiga)
            
        
    
    def test_desvincular_adolescente_com_saida_pendente(self):
        desv = Desvinculacao.objects.create(
            adolescente = self.AD_SAIDA_PENDENTE_UNIRE,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
        )
        
        try:
            desv.desvincular()    
        except:
            self.fail("desv.desvincular() levantou uma Exception!")
        
        self.assertEqual(desv.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_PENDENTE)
        self.assertEqual(self.AD_SAIDA_PENDENTE_UNIRE.entrada_em_unidade_atual, desv.entrada_antiga)
    
    
    def test_desvincular_adolescente_com_entrada_pendente(self):
        desv = Desvinculacao.objects.create(
            adolescente = self.AD_ENTRADA_PENDENTE_UNIRE,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
        )
        
        try:
            desv.desvincular()    
        except:
            self.fail("desv.desvincular() levantou uma Exception!")
        
        self.assertEqual(desv.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_REALIZADA)
        self.assertFalse(self.AD_ENTRADA_PENDENTE_UNIRE.possui_entrada_ativa)
        
    
    
    def test_desvincular_adolescente_lotado_em_geama(self):
        desv = Desvinculacao.objects.create(
            adolescente = self.AD_LOTADO_GEAMANB,
            data_saida = datetime.datetime.now(),
            tipo_saida = TipoSaidaUnidade.objects.first(),
        )
        
        try:
            desv.desvincular()    
        except:
            self.fail("desv.desvincular() levantou uma Exception!")
        
        self.assertEqual(desv.entrada_antiga.status, EntradaAdolescente.Status.SAIDA_REALIZADA)
        self.assertFalse(self.AD_LOTADO_GEAMANB.possui_entrada_ativa)