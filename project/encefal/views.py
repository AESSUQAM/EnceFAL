# -*- encoding: utf-8 -*-

# Changed render_to_response to render
# since it will not be supported by django 1.10

import json
import urllib
from lxml import html

from datetime import datetime, timedelta, date
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

from project.encefal.models import (
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

# Default employee index page
def index_employee(request):
    return render(request, 'encefal/employee/index.html', {},
                              RequestContext(request))

def acceuil(request):
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
                   'prix':exemplaire.prix,
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

def rapport(request):

    if 'date' in request.GET:
        date = request.GET['date']
        date = datetime.strptime(date,"%Y-%m-%d")
    else:
        date = datetime.today()

    lendemain = date + timedelta(days=1)

    # on met les deux dates a minuit
    date = date.replace(hour=0, minute=0, second=0)
    lendemain = lendemain.replace(hour=0, minute=0, second=0)

    ajoutes = Exemplaire.objects.all().filter(date_creation__gt=date,
                                              date_creation__lt=lendemain)
    factures = Facture.objects.all().filter(date_creation__gt=date,
                             date_creation__lt=lendemain)

    nb_ajoutes = ajoutes.count()
    nb_factures = factures.count()
    nb_vendus = sum([f.nb_livres() for f in factures])
    prix_total_vendu = sum([f.prix_total() for f in factures])

    context = {
        'nb_ajoutes':nb_ajoutes,
        'nb_factures':nb_factures,
        'date':date.date(),
        'nb_vendus':nb_vendus,
        'prix_total_vendu':prix_total_vendu,
    }

    return render(request, 'encefal/rapport.html', context)

def factures(request):

    #if not request.user.is_authenticated():
    #    return HttpResponseNotFound()

    if 'id' in request.GET and request.GET['id']:
        id_facture = request.GET['id']

        try:
            facture = Facture.objects.get(id=id_facture)
        except Facture.DoesNotExist:
            facture = None
    else:
        # Hack louche pour l'instant
        facture = 0

    context = {
        'facture':facture,
    }

    return render(request, 'encefal/factures.html', context)

