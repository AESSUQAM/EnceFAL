# -*- encoding: utf-8 -*-
import json
import urllib
from lxml import html

import datetime
from django.conf import settings
from django.shortcuts import render_to_response,render
from django.template import RequestContext, Context
from django.http import (
                         HttpResponseRedirect,
                         HttpResponse,
                         HttpResponseNotFound
                        )
from django.core.urlresolvers import reverse
from django.db.models import Sum, Q
from django.db.models import Count, Min, Sum, Avg
from django.forms.formsets import formset_factory

from models import (
                                    Facture,
                                    Livre,
                                    Session,
                                    Vendeur,
                                    ETAT_LIVRE_CHOICES,
                                    Exemplaire,
                                    ISBN_DB_BASE_QUERY,
                                    COOP_UQAM_BASE_QUERY
                                   )
from django.conf import settings

def accueil(request):
    return render(request, 'encefal/index.html',
{'next_session':Session.next_session(), 'current_session':Session.current_session()},
RequestContext(request))

def livres(request):

    livres = Livre.objects.all()
    livres = [livre for livre in livres if livre.nb_exemplaires_en_vente()]

    context = {
            'livres':livres,
            }

    return render(request, 'encefal/livres.html',
            context, context_instance = RequestContext(request))

def livre(request):

    if not request.user.is_authenticated():
        return HttpResponseNotFound()

	assert('isbn' in request.GET)
	assert('nb' in request.GET)
	assert(len(request.GET['isbn']) in [10,13])

	print("Assert done !")
	reponse = None
	livre = None
	isbn = request.GET['isbn']
	nb = request.GET['nb']

	try:
		livre = Livre.objects.get(isbn=isbn)
	except Livre.DoesNotExist:
		pass
	
	if not livre:
		query = ISBN_DB_BASE_QUERY.format(settings.ISBNDB_API_KEY, isbn)
		reponse_query = json.load(urllib.urlopen(query))
		if 'error' not in reponse_query:
			reponse_query = reponse_query['data'][0]

			titre = reponse_query['title'] if reponse_query['title'] else ''
			auteur = reponse_query['author_data'][0]['name'] if reponse_query['author_data'] else ''

			reponse = {'titre':titre,
					'auteur':auteur,
					'nb':nb}
		else:

			query = COOP_UQAM_BASE_QUERY.format(isbn)
			reponse_query = urllib.urlopen(query)
			tree = html.fromstring(reponse_query.read())

			titres = tree.cssselect("h3 a")
			if titres:

				titre = titres[0].text

				auteur = tree.cssselect("h3 + p")[0].text_content().split(' : ')[1].split('\r')[0].strip()

				reponse = {'titre':titre,
                           'auteur':auteur,
                           'nb':nb}

	else:
		reponse = {'titre':livre.titre,
				'auteur':livre.auteur,
                   'nb':nb}

	if reponse:
		return HttpResponse(json.dumps(reponse), content_type="application/json")
	else:
		return HttpResponseNotFound()
    try:
	    livre = Livre.objects.get(isbn=isbn)
    except Livre.DoesNotExist:
	    pass

    if not livre:
	    query = ISBN_DB_BASE_QUERY.format(settings.ISBNDB_API_KEY, isbn)
	    reponse_query = json.load(urllib.urlopen(query))
	    if 'error' not in reponse_query:
		    reponse_query = reponse_query['data'][0]

		    titre = reponse_query['title'] if reponse_query['title'] else ''
		    auteur = reponse_query['author_data'][0]['name'] if reponse_query['author_data'] else ''

		    reponse = {'titre':titre,
				    'auteur':auteur,
				    'nb':nb}
	    else:

		    query = COOP_UQAM_BASE_QUERY.format(isbn)
		    reponse_query = urllib.urlopen(query)
		    tree = html.fromstring(reponse_query.read())

		    titres = tree.cssselect("h3 a")
		    if titres:

			    titre = titres[0].text

			    auteur = tree.cssselect("h3 + p")[0].text_content().split(' : ')[1].split('\r')[0].strip()

			    reponse = {'titre':titre,
                           'auteur':auteur,
                           'nb':nb}

    else:
	    reponse = {'titre':livre.titre,
			    'auteur':livre.auteur,
                   'nb':nb}

    if reponse:
	    return HttpResponse(json.dumps(reponse), content_type="application/json")
    else:
	    return HttpResponseNotFound()

def exemplaire(request):

    if not request.user.is_authenticated():
        return HttpResponseNotFound()

	assert('identifiant' in request.GET)
	assert('nb' in request.GET)

    nb = request.GET['nb']
    identifiant = request.GET['identifiant']

    try:
        exemplaire = Exemplaire.objects.get(pk=identifiant)
    except Exemplaire.DoesNotExist:
        return HttpResponseNotFound()

	assert(exemplaire.livre)
	assert(exemplaire.livre)

    if exemplaire.etat != 'VENT':
        reponse = {
                   'status':'error',
                   'message':"L'exemplaire n'est pas en vente"
                  }
    else:
        reponse = {
                   'status':'ok',
                   'titre':exemplaire.livre.titre,
                   'auteur':exemplaire.livre.auteur,
                   'prix':float(exemplaire.prix),
                   'isbn':exemplaire.livre.isbn,
                   'nb':nb
                  }

    return HttpResponse(json.dumps(reponse), content_type="application/json")

def vendeur(request):

    if not request.user.is_authenticated():
        return HttpResponseNotFound()

    assert('code' in request.GET)
    assert(len(request.GET['code']) == 12)

    vendeur = None
    code = request.GET['code']

    try:
        vendeur = Vendeur.objects.get(code_permanent=code)
    except Vendeur.DoesNotExist:
        return HttpResponseNotFound()

    reponse = {
               'nom':vendeur.nom,
               'prenom':vendeur.prenom,
               'telephone':vendeur.telephone,
               'email':vendeur.email
              }

    return HttpResponse(json.dumps(reponse), content_type="application/json")

def factures(request):

    if not request.user.is_authenticated():
        return HttpResponseNotFound()

	if not request.user.is_authenticated():
		return HttpResponseNotFound()

	if 'id' in request.GET and request.GET['id']:
		id_facture = request.GET['id']

		try:
			id_facture = int(id_facture)

			try:
				facture = Facture.objects.get(id=id_facture)
			except Facture.DoesNotExist:
				facture = None
		except:
			facture = None

	else:
		# Hack louche pour l'instant
		facture = 0

	context = {
		'facture':facture,
		'taxable':settings.TAXABLES,
	}

	return render(request, 'encefal/factures.html', context)

def livresVendeur(request):
	context={}

	if 'code_perm' in request.GET and request.GET['code_perm']:
		code_vend = request.GET['code_perm']

		# Afficher recu
		try:
		    vendeur = Vendeur.objects.get(code_permanent=code_vend)
		    context['vendeur'] = vendeur
		    context['exemplaires'] = vendeur.exemplaires.all()

		except Vendeur.DoesNotExist:
		    context['vendeur'] = None
		    context['exemplaires'] = []

		context['date_transaction'] = datetime.date.today()
		context['employe'] = 'Non-disponible'
		context['montant_total'] = sum([e.prix for e in context['exemplaires']]) or 0

	context['from_view']=True
	context['ext']='base.html'

	return render(request, 'encefal/depots.html', context)

