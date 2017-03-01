# Todo, to get some help on how to test the admin site goto :
# https://github.com/django/django/blob/master/tests/modeladmin/tests.py#L14

from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from main.models import *
from employee.admin import *

class MockRequest(object):
    pass


class MockSuperUser(object):

    def has_perm(self, perm):
        return true

request = MockRequest()
request.user = MockSuperUser()


class ModelAdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.vendeur = Vendeur.objects.create(
            nom="Robert",
            prenom="Bob",
            code_permanent="ROBB11223300",
            email="bob.robert@truc.org"
        )
        self.recep_inline = ExemplaireReceptionInline(Exemplaire, self.site)
        self.vente_inline = ExemplaireVenteInline(Exemplaire, self.site)
        self.sess_admin = SessionAdmin(Session, self.site)
        self.rece_admin = ReceptionAdmin(Reception, self.site)

    def test_recepInlineExclude(self):
        self.assertIsNotNone(self.recep_inline.exclude)
        self.assertTrue("facture" in self.recep_inline.exclude)
        self.assertTrue("livre" in self.recep_inline.exclude)

    def test_recepInlineFields(self):
        self.assertIsNotNone(self.recep_inline.fields)
        self.assertTrue("isbn" in self.recep_inline.fields)
        self.assertTrue("prix" in self.recep_inline.fields)

    def test_receptInlineRest(self):
        self.assertIsNotNone(self.recep_inline.model)
        self.assertIsNotNone(self.recep_inline.form)
        self.assertIsNotNone(self.recep_inline.extra)
        self.assertEqual(self.recep_inline.extra, 5)

    def test_venteInlineExclude(self):
        self.assertIsNotNone(self.vente_inline.exclude)
        self.assertTrue("actif" in self.vente_inline.exclude)
        self.assertTrue("livre" in self.vente_inline.exclude)

    def test_venteInlineFields(self):
        self.assertIsNotNone(self.vente_inline.fields)
        self.assertTrue("identifiant" in self.vente_inline.fields)
        self.assertTrue("prix" in self.vente_inline.fields)

    def test_ventetInlineRest(self):
        self.assertIsNotNone(self.vente_inline.model)
        self.assertIsNotNone(self.vente_inline.form)
        self.assertIsNotNone(self.vente_inline.extra)
        self.assertEqual(self.vente_inline.extra, 5)

    def test_sessAdminExclude(self):
        self.assertIsNotNone(self.sess_admin.exclude)
        self.assertTrue("actif" in self.sess_admin.exclude)

    def test_sessAdminList(self):
        self.assertIsNotNone(self.sess_admin.list_display)
        self.assertTrue("nom" in self.sess_admin.list_display)
        self.assertTrue("date_fin" in self.sess_admin.list_display)

    def test_recAdminMemberCheck(self):
        self.assertIsNotNone(self.rece_admin.exclude)
        self.assertIsNotNone(self.rece_admin.fields)
        self.assertIsNotNone(self.rece_admin.inlines)
        self.assertIsNotNone(self.rece_admin.list_display)
        self.assertIsNotNone(self.rece_admin.model)
        self.assertTrue('code_permanent' in self.rece_admin.fields)
        self.assertTrue('telephone' in self.rece_admin.fields)
        self.assertTrue('actif' in self.rece_admin.exclude)
        self.assertTrue('date_creation' in self.rece_admin.list_display)
        self.assertTrue('code_permanent' in self.rece_admin.list_display)

    def test_recAdminSaveNew(self):
        obj = Vendeur.objects.create(code_permanent="LAVJ22119401")

        # Should create a new object Vendeur
        self.rece_admin.save_model(None, obj, None, None)

        try:
            Vendeur.objects.get(code_permanent=obj.code_permanent)
            self.assertTrue(True)
        except Vendeur.DoesNotExist:
            fail()

    def test_recAdminResponseAdd(self):
        class t:
            def all(self):
                return []

        class a:
            pk = None
            code_permanent = "LAVJ22119402"
            exemplaires = t()

        class u:
            username="Jo"


        class b:
            user = u()

        obj = a()
        resp = self.rece_admin.response_add(b(), obj)
        resp2 = self.rece_admin.response_add(b(), obj)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, resp2.status_code)
