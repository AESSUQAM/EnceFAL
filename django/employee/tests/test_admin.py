# Todo, to get some help on how to test the admin site goto :
# https://github.com/django/django/blob/master/tests/modeladmin/tests.py#L14

from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from main.models import *

# Create your tests here.


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
        self.recep_inline = ExemplaireReceptionInline()
        self.vente_inline = ExemplaireVenteInline()
        self.sess_admin = SessionAdmin()

    def recepInlineExclude(self):
        assertIsNotNone(self.recep_inline.exclude)
        assertTrue("facture" in self.recep_inline.exclude)
        assertTrue("livre" in self.recep_inline.exclude)

    def recepInlineFields(self):
        assertIsNotNone(self.recep_inline.fields)
        assertTrue("isbn" in self.recep_inline.fields)
        assertTrue("prix" in self.recep_inline.fields)

    def receptInlineRest(self):
        assertIsNotNone(self.recep_inline.model)
        assertIsNotNone(self.recep_inline.form)
        assertIsNotNone(self.recep_inline.extra)
        assertEqual(self.recep_inline.extra, 5)

    def venteInlineExclude(self):
        assertIsNotNone(self.vente_inline.exclude)
        assertTrue("actif" in self.vente_inline.exclude)
        assertTrue("livre" in self.vente_inline.exclude)

    def venteInlineFields(self):
        assertIsNotNone(self.vente_inline.fields)
        assertTrue("identifiant" in self.vente_inline.fields)
        assertTrue("prix" in self.vente_inline.fields)

    def ventetInlineRest(self):
        assertIsNotNone(self.vente_inline.model)
        assertIsNotNone(self.vente_inline.form)
        assertIsNotNone(self.vente_inline.extra)
        assertEqual(self.vente_inline.extra, 5)

    def sessAdminExclude(self):
        assertIsNotNone(self.sess_admin.exclude)
        assertTrue("actif" in self.sess_admin.exclude)

    def sessAdminList(self):
        assertIsNotNone(self.sess_admin.list_display)
        assertTrue("nom" in self.sess_admin.list_display)
        assertTrue("date_fin" in self.sess_admin.list_display)
