from decimal import Decimal
from django.test import TestCase
from geoposition import Geoposition
from unidades.models import Unidade
from dominios.models import Uf, Cidade, Bairro, TipoUnidade, RegulamentoInfracoes

class GeopositionTestCase(TestCase):
    fixtures = ['fixtures/base/1-dominios.json']
    
    def test_init_with_decimals(self):
        gp = Geoposition(Decimal('52.5'), Decimal('13.4'))
        self.assertEqual(gp.latitude, Decimal('52.5'))
        self.assertEqual(gp.longitude, Decimal('13.4'))

    def test_init_with_strs(self):
        gp = Geoposition('52.5', '13.4')
        self.assertEqual(gp.latitude, Decimal('52.5'))
        self.assertEqual(gp.longitude, Decimal('13.4'))

    def test_init_with_floats(self):
        gp = Geoposition(52.5, 13.4)
        self.assertEqual(gp.latitude, Decimal('52.5'))
        self.assertEqual(gp.longitude, Decimal('13.4'))

    def test_repr(self):
        gp = Geoposition(52.5, 13.4)
        self.assertEqual(repr(gp), 'Geoposition(52.5,13.4)')

    def test_len(self):
        gp = Geoposition(52.5, 13.4)
        self.assertEqual(len(gp), 9)

    def test_equality(self):
        gp1 = Geoposition(52.5, 13.4)
        gp2 = Geoposition(52.5, 13.4)
        self.assertEqual(gp1, gp2)

    def test_inequality(self):
        gp1 = Geoposition(52.5, 13.4)
        gp2 = Geoposition(52.4, 13.1)
        self.assertNotEqual(gp1, gp2)

    def test_equality_with_none(self):
        gp1 = Geoposition(52.5, 13.4)
        gp2 = None
        self.assertFalse(gp1 == gp2)

    def test_inequality_with_none(self):
        gp1 = Geoposition(52.5, 13.4)
        gp2 = None
        self.assertTrue(gp1 != gp2)

    def test_db_value_to_python_object(self):
        uf = Uf.objects.get(sigla='DF')
        cidade = uf.cidades.first()
        bairro = cidade.bairros.first()
        
        obj = Unidade.objects.create(
            nome='Unidade Fake',
            sigla='UNIFAKE',
            tipo_unidade = TipoUnidade.objects.first(),
            uf = uf,
            cidade = cidade,
            bairro = bairro,
            regulamento_infracoes = RegulamentoInfracoes.objects.first(),
            localizacao=Geoposition(52.5, 13.4)
        )
        poi = Unidade.objects.get(id=obj.id)
        self.assertIsInstance(poi.localizacao, Geoposition)
