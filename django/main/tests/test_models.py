# -*- encoding: utf-8 -*-

from django.conf import settings
from django.test import TestCase, Client
from django.core import mail
from django.forms import ValidationError
from main.models import *

import datetime
from decimal import Decimal

class ModelsTest(TestCase):
    def setUp(self):
        # Test statique de session avant la creation
        self.assertIsNone(Session.current_session())
        self.assertIsNone(Session.next_session())


        self.user = User.objects.create_user(
            username='abc', email='abc@123.com', password='test123')

        v = Vendeur.objects.create(nom="Robert", prenom="Bob", code_permanent="ROBB11223300", email="bob.robert@truc.org")
        l =	Livre.objects.create(titre="abc123")

        ddeb = datetime.date.today()
        dfin = ddeb + datetime.timedelta(1, 0)
        s = Session.objects.create(nom="Test", date_debut=ddeb, date_fin=dfin)

        fact = Facture.objects.create(employe=self.user, session=s)

        e = Exemplaire.objects.create(livre=l, vendeur=v, etat="VENT", prix='10.05', facture=fact)



    def testVendeur(self):
        # Teste les fonctionalite du vendeur
        Vendeur.objects.create(nom="Test", prenom="Cas",
					         		code_permanent="TESC00000000",
							        email="test.cas@test.com",
							        telephone="(123) 000-1234")

        self.assertIsNotNone(Vendeur.objects.get(nom="Test"))
        vend = Vendeur.objects.get(nom="Test")

        # Test des Fields
        self.assertEqual(vend.nom, "Test")
        self.assertEqual(vend.prenom, "Cas")
        self.assertEqual(vend.code_permanent, "TESC00000000")
        self.assertEqual(vend.email, "test.cas@test.com")
        self.assertEqual(vend.telephone, "(123) 000-1234")
        self.assertTrue("Test, Cas" in vend.__unicode__())
        self.assertEqual(vend.nb_livres.short_description, 'Nombre de livres')

        # Test du email
        vend.envoyer_recu()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'contrat')
        self.assertEqual(mail.outbox[0].from_email, 'aess@aessuqam.org')
        self.assertTrue(vend.email in mail.outbox[0].to)
        self.assertTrue(mail.outbox[0].message > 1)


    def testSession(self):
        # Teste les fonctionalite de Session
        sess = Session.objects.get(nom="Test")

        self.assertTrue("Test" in sess.__unicode__())
        self.assertIsNotNone(sess.next_session())
        self.assertTrue(sess.current_session() == sess)

        self.assertIsNotNone(sess.next_session())


    def testExemplaire(self):

        print("Creating objects...")
        vend = Vendeur.objects.get(nom="Robert")
        vend.save()

        liv = Livre.objects.get(titre="abc123")
        liv.save()

        # Test de creation d'exemplaire avec un prix invalide
        print("Creating with price 10.03")
        exemp = Exemplaire.objects.create(livre=liv, vendeur=vend, etat='VENT', prix='10.03')
        self.assertRaises(ValidationError, lambda: exemp.full_clean())

        # Test de creation d'exemplaire avec un prix valide
        print("Creating with price 10.05")
        exemp = Exemplaire.objects.create(livre=liv, vendeur=vend, etat="VENT", prix='10.05')
        exemp.full_clean()
        exemp.save()

        self.assertTrue(liv.titre in exemp.__unicode__())
        self.assertEqual(exemp.titre(), liv.titre)
        self.assertEqual(exemp.code_permanent_vendeur(), vend.code_permanent)

        print("Objects created")


    def testFacture(self):
        sess = Session.objects.get(nom="Test")
        fact = Facture.objects.get(session=sess)

        self.assertTrue('1' in fact.__unicode__())
        self.assertEqual(fact.nb_livres(), 1)
        self.assertEqual(fact.prix_avant_taxes(), 10.05)

        if settings.TAXABLES:
            self.assertTrue(0.4 < fact.prix_tps() < 0.6)
            self.assertTrue(1 < fact.prix_tvq() < 1.05)
            self.assertEqual(fact.prix_total(), 11.55)

    # Test de quelques methodes
    def testDatabase(self):

        print("Testing previously created objects...")

        # Recuperation des objets précédemment créé
        vend = Vendeur.objects.get(nom="Robert")
        liv = Livre.objects.get(titre="abc123")
        exe = Exemplaire.objects.create(livre=liv, vendeur=vend, etat="VENT", prix='10.05')

        # Assert des fonctions de ces objets
        self.assertEqual(vend.nb_livres(), 2)
        self.assertEqual(liv.nb_exemplaires_en_vente(), 2)
        self.assertEqual(liv.prix_moyen(), Decimal('10.05'))
        self.assertEqual(exe.vendeur, vend)

        # Assert des fonctions de ces objets
        self.assertEqual(vend.nb_livres(), 2)
        self.assertEqual(liv.nb_exemplaires_en_vente(), 2)
        self.assertEqual(liv.prix_moyen(), Decimal('10.05'))
        self.assertEqual(exe.vendeur, vend)
