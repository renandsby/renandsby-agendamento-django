from datetime import datetime
from django.test import TestCase
from django.core.management import call_command
from dominios.models import TipoUnidade
from adolescentes.models import Adolescente
from processos.models import Processo
from unidades.models import Unidade, EntradaAdolescente, Quarto, Modulo
from django.core.exceptions import ValidationError
import datetime 

class UnidadesTestCase(TestCase):
    fixtures = [
        'fixtures/base/1-dominios.json', 
        'fixtures/base/4-base_unidades.json',
    ]

    @classmethod
    def setUpTestData(cls):
        ''' Isso aqui roda uma vez só antes de todos os testes '''
        cls.UNIRE = Unidade.objects.get(sigla='UNIRE')
        cls.UIBRA = Unidade.objects.get(sigla='UIBRA')
        cls.GERSEMIMET = Unidade.objects.get(sigla='GERSEMIMET')
        cls.GEAMANB = Unidade.objects.get(sigla='GEAMANB')
        
        cls.ADOLESCENTE = Adolescente.objects.create(
            nome="ADOLESCENTE", 
            data_nascimento=datetime.datetime.now(), 
            cor_id=1, 
            genero_id=1
        )
        cls.OUTRO_ADOLESCENTE = Adolescente.objects.create(
            nome="OUTRO ADOLESCENTE", 
            data_nascimento=datetime.datetime.now(), 
            cor_id=1, 
            genero_id=1
        )
        Processo.objects.create(adolescente = cls.ADOLESCENTE, numero = "1234516" )
        Processo.objects.create(adolescente = cls.OUTRO_ADOLESCENTE, numero = "1234516" )

    def setUp(self):
        ''' Isso aqui roda antes de cada teste '''
        ...

    # não permite processo que não seja do adolescente selecionado
    def test_nao_permite_processo_de_adol_diferente(self):
        with self.assertRaises(ValidationError):
            EntradaAdolescente.objects.create(
                adolescente = self.ADOLESCENTE,    
                unidade = self.UNIRE,
                processo = self.OUTRO_ADOLESCENTE.processos.first()
            )
        
        with self.assertRaises(ValidationError):
            entrada = EntradaAdolescente.objects.create(
                adolescente = self.ADOLESCENTE,    
                unidade = self.UNIRE,
                processo = self.OUTRO_ADOLESCENTE.processos.first()
            )
            entrada.save()
        
    def test_status_default_entrada_pendente(self):
        try: 
            e = EntradaAdolescente.objects.create(
                    adolescente = self.ADOLESCENTE,    
                    unidade = self.UNIRE,
                    processo = self.ADOLESCENTE.processos.first()
            )
        except:
            self.fail('Não foi possível criar entrada do adolescente.')
        
        self.assertEqual(e.status, EntradaAdolescente.Status.ENTRADA_PENDENTE)
    
    def test_nao_permite_duas_entradas_pendentes(self):
        with self.assertRaises(ValidationError):
            EntradaAdolescente.objects.create(
                adolescente = self.ADOLESCENTE,    
                unidade = self.UNIRE,
                processo = self.ADOLESCENTE.processos.first(),
                status = EntradaAdolescente.Status.ENTRADA_PENDENTE
            )
            
            EntradaAdolescente.objects.create(
                adolescente = self.ADOLESCENTE,    
                unidade = self.GERSEMIMET,
                processo = self.ADOLESCENTE.processos.first(),
                status = EntradaAdolescente.Status.ENTRADA_PENDENTE
            )
    def test_nao_permite_entrada_pendente_com_realizada(self):
        with self.assertRaises(ValidationError):
            EntradaAdolescente.objects.create(
                adolescente = self.ADOLESCENTE,    
                unidade = self.UNIRE,
                processo = self.ADOLESCENTE.processos.first(),
                status = EntradaAdolescente.Status.ENTRADA_PENDENTE
            )
            
            EntradaAdolescente.objects.create(
                adolescente = self.ADOLESCENTE,    
                unidade = self.GERSEMIMET,
                processo = self.ADOLESCENTE.processos.first(),
                status = EntradaAdolescente.Status.ENTRADA_REALIZADA
            )
            
    def test_nao_permite_duas_entradas_lotado(self):
        with self.assertRaises(ValidationError):
            EntradaAdolescente.objects.create(
                adolescente = self.ADOLESCENTE,    
                unidade = self.GERSEMIMET,
                quarto = self.GERSEMIMET.modulos.first().quartos.first(),
                processo = self.ADOLESCENTE.processos.first(),
                status = EntradaAdolescente.Status.SAIDA_PENDENTE
            )

            EntradaAdolescente.objects.create(
                adolescente = self.ADOLESCENTE,    
                unidade = self.UNIRE,
                modulo = self.UNIRE.modulos.first(),
                quarto = self.UNIRE.modulos.first().quartos.first(),
                processo = self.ADOLESCENTE.processos.first(),
                status = EntradaAdolescente.Status.ENTRADA_REALIZADA
            )
        
    
    
        
