# -*- encoding: utf-8 -*-
from django.conf.urls import *
from main.views import *

urlpatterns = [
    url(r'^$', accueil, name='accueil'),
    url(r'^livres/$', livres, name='livres'),
    url(r'^livre/$', livre, name='livre'),
    url(r'^exemplaire/$', exemplaire, name='exemplaire'),
    url(r'^vendeur/$', vendeur, name='vendeur'),
    url(r'^factures/$', factures, name='factures'),
	url(r'^livre_vendeur/$', livresVendeur, name='livres_vendeur'),
]
